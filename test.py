import streamlit as st

# Hardcoded credentials (replace with a database for production)
USER_CREDENTIALS = {
    "admin": "password123",
    "user1": "pass456",
    "user2": "mypassword"
}

# Function to check login credentials
def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return True
    return False

# Main function
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Login")

        # Login form
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

        if submit:
            if login(username, password):
                st.success(f"Welcome, {username}!")
                st.session_state.logged_in = True
            else:
                st.error("Invalid username or password.")
    else:
        # Logged-in view
        st.title("Welcome to the App!")
        st.sidebar.button("Logout", on_click=logout)

def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()  # Refresh the page after logging out

# Run the app
if __name__ == "__main__":
    main()
