import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="Digital Visiting Card",
    page_icon="👋",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .css-1v0mbdj.etr89bj1 {
        display: block;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }
    
    .profile-img {
        border-radius: 50%;
        border: 4px solid white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .social-links {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }
    
    .contact-item {
        background-color: #f8f9fa;
        padding: 10px 20px;
        border-radius: 10px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .contact-item:hover {
        background-color: #e9ecef;
        transform: translateX(5px);
    }
    
    .name-header {
        color: #1f2937;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0;
    }
    
    .title-text {
        color: #4b5563;
        font-size: 1.2em;
        margin-top: 5px;
    }
    
    .company-text {
        color: #6b7280;
        font-size: 1.1em;
        margin-top: 5px;
    }
    
    .badge {
        background-color: #e5e7eb;
        color: #374151;
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Mock user data (in a real application, this could come from a database or API)
user_data = {
    "name": "Niwesh Sah",
    "title": "Student",
    "company": "IIT Mandi",
    "email": "sahniwesh@gmail.com",
    "phone": "+91 9451864348",
    "website": "www.niweshsah.dev",
    "location": "San Francisco, CA",
    "github": "niweshsah",
    "linkedin": "niwesh-sah-86b9a027b",
    "avatar_url": "https://api.dicebear.com/6.x/initials/svg?seed=NS"  # Using DiceBear for demo avatar
}

# Function to load and process avatar image
def get_avatar_image():
    try:
        response = requests.get(user_data["avatar_url"])
        return BytesIO(response.content)
    except:
        # Fallback to a default avatar or handle error
        return None

# Main container with gradient background
with st.container():
    # Center column layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Profile Image
        avatar = get_avatar_image()
        if avatar:
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="{user_data['avatar_url']}" 
                         class="profile-img"
                         width="150px"
                         height="150px">
                </div>
            """, unsafe_allow_html=True)

        # Name and Title
        st.markdown(f"""
            <h1 class="name-header">{user_data['name']}</h1>
            <div class="badge">{user_data['title']}</div>
            <p class="company-text">🏢 {user_data['company']}</p>
        """, unsafe_allow_html=True)

        # Contact Information
        st.markdown("---")
        
        # Email
        st.markdown(f"""
            <div class="contact-item">
                📧 <a href="mailto:{user_data['email']}">{user_data['email']}</a>
            </div>
        """, unsafe_allow_html=True)
        
        # Phone
        st.markdown(f"""
            <div class="contact-item">
                📱 <a href="tel:{user_data['phone']}">{user_data['phone']}</a>
            </div>
        """, unsafe_allow_html=True)
        
        # Website
        st.markdown(f"""
            <div class="contact-item">
                🌐 <a href="https://{user_data['website']}" target="_blank">{user_data['website']}</a>
            </div>
        """, unsafe_allow_html=True)
        
        # Location
        st.markdown(f"""
            <div class="contact-item">
                📍 {user_data['location']}
            </div>
        """, unsafe_allow_html=True)

        # Social Links
        st.markdown("---")
        st.markdown(f"""
            <div class="social-links">
                <a href="https://github.com/{user_data['github']}" target="_blank">
                    <img src="https://img.shields.io/badge/GitHub-%2312100E.svg?&style=for-the-badge&logo=Github&logoColor=white" />
                </a>
                <a href="https://www.linkedin.com/in/{user_data['linkedin']}" target="_blank">
                    <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />
                </a>
            </div>
        """, unsafe_allow_html=True)

# Add some interactivity
if st.button("💾 Save Contact"):
    # Generate vCard data
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{user_data['name']}
TITLE:{user_data['title']}
ORG:{user_data['company']}
EMAIL:{user_data['email']}
TEL:{user_data['phone']}
URL:{user_data['website']}
ADR;TYPE=WORK:{user_data['location']}
END:VCARD"""
    
    # Create download button for vCard
    b64_vcard = base64.b64encode(vcard.encode()).decode()
    href = f'<a href="data:text/vcard;base64,{b64_vcard}" download="contact.vcf">📥 Download vCard</a>'
    st.markdown(href, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: #6b7280; font-size: 0.8em;'>
        Made with ❤️ using Streamlit
    </p>
""", unsafe_allow_html=True)