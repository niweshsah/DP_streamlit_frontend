import streamlit as st
import requests
from datetime import datetime, timedelta

def main_food():
    # Streamlit page configuration
    # st.set_page_config(page_title="Conference Food Management", layout="centered")

    # Define API URL
    API_BASE_URL = "http://localhost:27017/user/conference"

    def check_conference_exists(conference_code):
        """Helper function to check if conference exists"""
        try:
            response = requests.get(f"{API_BASE_URL}/{conference_code}/checkConferenceCode")
            # print("status code: ",response.status_code )
            return response.status_code == 200, response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException:
            return False, None

    def check_food_items(conference_code):
        """Helper function to check if food items exist"""
        try:
            response = requests.get(f"{API_BASE_URL}/{conference_code}/eventCard/food")
            if response.status_code == 200:
                foods = response.json().get('data', [])
                return len(foods) > 0, foods
            return False, []
        except requests.exceptions.RequestException:
            return False, []

    # Conference Code input with validation
    # conference_code = st.text_input("Conference Code", placeholder="Enter conference code")
    
    
    conference_code = st.session_state.get('current_user', 'Guest')
    print(f"Hello, {conference_code}!")

    if conference_code:
        conference_exists, conference_data = check_conference_exists(conference_code)
        if not conference_exists:
            st.error("❌ Conference not found! Please check the conference code.")
            st.info("💡 Make sure you have entered the correct conference code")
            return
        else:
            st.success(f"✅ Connected to conference: {conference_data.get('name', conference_code)}")
            if conference_data.get('location'):
                st.info(f"📍 Location: {conference_data['location']}")
    else:
        st.warning("Please enter a conference code to proceed.")
        return

    # Select operation
    operation = st.radio("Choose an operation:", ["Add Food Item", "Delete Food Item", "View Food Items"])

    def time_input_widget(label):
        st.subheader(label)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date = st.date_input(f"{label} Date")
        with col2:
            hour = st.selectbox(
                f"{label} Hour", 
                list(range(0, 24)), 
                format_func=lambda x: f"{x:02}",
                key=f"hour_{label}"
            )
        with col3:
            minute = st.selectbox(
                f"{label} Minute", 
                list(range(0, 60)), 
                format_func=lambda x: f"{x:02}",
                key=f"minute_{label}"
            )
            
        return datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute))

    # Add Food Item Operation
    if operation == "Add Food Item":
        st.header("Add New Food Item")

        # Show conference dates if available
        if conference_data.get('startDate') and conference_data.get('endDate'):
            conf_start = datetime.fromisoformat(conference_data['startDate'].replace('Z', ''))
            conf_end = datetime.fromisoformat(conference_data['endDate'].replace('Z', ''))
            st.info(f"Conference Duration: {conf_start.strftime('%Y-%m-%d')} to {conf_end.strftime('%Y-%m-%d')}")

        # Food details input
        food_name = st.text_input("Food Name", placeholder="Enter food name")
        food_description = st.text_area("Food Description", placeholder="Enter food description")
        
        # Time inputs
        start_time = time_input_widget("Start Time")
        expiry_time = time_input_widget("Expiry Time")

        # Show current food count
        has_foods, current_foods = check_food_items(conference_code)
        if has_foods:
            st.info(f"Currently {len(current_foods)} food items in the conference")
        else:
            st.info("No food items yet in this conference")

        # Validation and submission
        if st.button("Submit Food Item"):
            if food_name:
                if expiry_time <= start_time:
                    st.error("❌ Expiry time must be after start time!")
                else:
                    # Additional validation against conference dates if available
                    if conference_data.get('startDate') and conference_data.get('endDate'):
                        conf_start = datetime.fromisoformat(conference_data['startDate'].replace('Z', ''))
                        conf_end = datetime.fromisoformat(conference_data['endDate'].replace('Z', ''))
                        
                        if start_time < conf_start or expiry_time > conf_end:
                            st.error("❌ Food timing must be within conference dates!")
                            return

                    food_data = {
                        "name": food_name,
                        "description": food_description,
                        "startTime": start_time.isoformat(),
                        "expiryTime": expiry_time.isoformat()
                    }

                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/{conference_code}/eventCard/food",
                            json=food_data
                        )
                        
                        if response.status_code in [200, 201]:
                            st.success(f"✅ Food item '{food_name}' added successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to add food item: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error connecting to server: {str(e)}")
            else:
                st.error("❌ Please enter at least the food name!")

    # Delete Food Item Operation
    elif operation == "Delete Food Item":
        st.header("Delete Food Item")

        # Check for existing food items
        has_foods, foods = check_food_items(conference_code)
        
        if not has_foods:
            st.warning("⚠️ No food items available in this conference")
            st.info("💡 Add some food items first using the 'Add Food Item' option")
            return

        # Show delete interface only if there are foods
        food_names = [food['name'] for food in foods]
        selected_food = st.selectbox("Select Food Item to Delete", food_names)
        
        if st.button("Delete Selected Food Item"):
            try:
                response = requests.delete(
                    f"{API_BASE_URL}/{conference_code}/eventCard/food/{selected_food}"
                )
                
                if response.status_code == 200:
                    st.success(f"✅ Food item '{selected_food}' deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to delete food item: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error connecting to server: {str(e)}")

    # View Food Items
    elif operation == "View Food Items":
        st.header("Current Food Items")
        
        try:
            response = requests.get(f"{API_BASE_URL}/{conference_code}/eventCard/food")
            if response.status_code == 200:
                foods = response.json().get('data', [])
                
                if not foods:
                    st.warning("⚠️ No food items found in this conference")
                    st.info("💡 You can add food items using the 'Add Food Item' option")
                    
                    # Display a helpful message about what can be added
                    with st.expander("ℹ️ What can I add?"):
                        st.write("""
                        You can add food items with the following information:
                        - Name of the food item
                        - Description
                        - Start time (when the food will be available)
                        - Expiry time (when the food should be consumed by)
                        """)
                else:
                    st.success(f"✅ Found {len(foods)} food items")
                    for food in foods:
                        with st.expander(f"🍽️ {food['name']}"):
                            st.write(f"📝 Description: {food.get('description', 'No description provided')}")
                            if food.get('startTime'):
                                st.write(f"⏰ Start Time: {datetime.fromisoformat(food['startTime'].replace('Z', '')).strftime('%Y-%m-%d %I:%M %p')}")
                            if food.get('expiryTime'):
                                st.write(f"⚠️ Expiry Time: {datetime.fromisoformat(food['expiryTime'].replace('Z', '')).strftime('%Y-%m-%d %I:%M %p')}")
            else:
                st.error("❌ Failed to fetch food items. Please check the conference code and try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error connecting to server: {str(e)}")

if __name__ == "__main__":
    main_food()