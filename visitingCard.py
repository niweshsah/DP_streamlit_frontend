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
    /* Main Container */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Profile Image */
    .profile-img {
        border-radius: 50%;
        border: 4px solid white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 150px;
        height: 150px;
        object-fit: cover;
    }
    
    /* Name and Title */
    .name-header {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0;
        color: #1f2937;
    }
    
    .title-text {
        font-size: 1.2em;
        margin-top: 5px;
        color: #4b5563;
    }
    
    .company-text {
        font-size: 1.1em;
        margin-top: 5px;
        color: #6b7280;
    }
    
    /* Contact Information */
    .contact-item {
        background-color: #f8f9fa;
        padding: 10px 20px;
        border-radius: 10px;
        margin: 10px 0;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .contact-item:hover {
        background-color: #e9ecef;
        transform: translateX(5px);
    }
    
    /* Social Links */
    .social-links {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }
    
    /* Buttons */
    .button {
        background-color: #4CAF50;
        color: #fff;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    
    .button:hover {
        background-color: #3e8e41;
    }
    
    /* Footer */
    .footer {
        font-size: 0.8em;
        color: #6b7280;
        text-align: center;
        margin-top: 20px;
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
            <div class="title-text">{user_data['title']}</div>
            <div class="company-text">{user_data['company']}</div>
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
        
        st.markdown("""
    <style>
        div.stButton > button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        div.stButton > button:hover {
            background-color: #3e8e41;
        }
    </style>
""", unsafe_allow_html=True)


                # Modified save contact functionality
        if st.button("📱 Save to Android Phone", key="save_contact"):
    # Generate Android-compatible vCard
    # Note: Using VERSION:2.1 for better Android compatibility
            vcard = [
                "BEGIN:VCARD",
                "VERSION:2.1",  # Changed to 2.1 for better Android support
                f"N;CHARSET=UTF-8:{user_data['name'].split()[-1]};{' '.join(user_data['name'].split()[:-1])}",
                f"FN;CHARSET=UTF-8:{user_data['name']}",
                f"ORG;CHARSET=UTF-8:{user_data['company']}",
                f"TITLE;CHARSET=UTF-8:{user_data['title']}",
                f"TEL;CELL:{user_data['phone'].replace(' ', '').replace('+', '')}",  # Remove spaces and + from phone
                f"EMAIL;INTERNET:{user_data['email']}",
                f"URL:{user_data['website']}",
                f"ADR;HOME;CHARSET=UTF-8:;;{user_data['location']}",
                f"X-GITHUB:{user_data['github']}",
                f"X-LINKEDIN:{user_data['linkedin']}",
                "END:VCARD"
            ]
            
            # Join with proper line endings (\r\n for vCard spec)
            vcard_text = "\r\n".join(vcard) + "\r\n"
            
            # Create download link with specific Android mime-type
            b64_vcard = base64.b64encode(vcard_text.encode('utf-8')).decode()
            
            st.markdown(
                f'''
                <div style="text-align: center; margin-top: 20px;">
                    <a href="data:text/x-vcard;charset=utf-8;base64,{b64_vcard}" 
                    download="contact.vcf"
                    style="text-decoration: none;">
                        <button style="
                            background-color: #4CAF50;
                            color: white;
                            padding: 12px 24px;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 16px;
                            display: inline-flex;
                            align-items: center;
                            gap: 8px;">
                            <span>📥</span> Download Contact (Android)
                        </button>
                    </a>
                    <p style="margin-top: 10px; color: #666; font-size: 14px;">
                        Android Instructions:<br>
                        1. Click the button above<br>
                        2. Open the downloaded file (usually in Downloads folder)<br>
                        3. Select "Contacts" app when prompted<br>
                        4. Confirm adding the contact
                    </p>
                </div>
                ''',
                unsafe_allow_html=True
            )

            # Add a direct "Share to Contacts" intent for Android
            st.markdown(
                f'''
                <div style="text-align: center; margin-top: 20px;">
                    <a href="intent:#Intent;action=android.intent.action.VIEW;type=text/x-vcard;S.vcard={b64_vcard};end" 
                    style="text-decoration: none;">
                        <button style="
                            background-color: #2196F3;
                            color: white;
                            padding: 12px 24px;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 16px;
                            display: inline-flex;
                            align-items: center;
                            gap: 8px;">
                            <span>📲</span> Open Directly in Contacts
                        </button>
                    </a>
                </div>
                ''',
                unsafe_allow_html=True
            )