# import streamlit as st
# from PIL import Image
# import requests
# from io import BytesIO
# import base64
# import json

# # Page configuration
# st.set_page_config(
#     page_title="Digital Visiting Card",
#     page_icon="🪪",
#     layout="centered"
# )

# # Enhanced Custom CSS with better color schemes and transitions
# st.markdown("""
# <style>
#     /* Global Styles */
#     * {
#         transition: all 0.3s ease-in-out;
#     }
    
#     /* Main Container */
#     .main-container {
#         max-width: 800px;
#         margin: auto;
#         padding: 2rem;
#         border-radius: 16px;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
#     }
    
#     /* Profile Image */
#     .profile-img {
#         border-radius: 50%;
#         margin: auto;
#         display: block;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#         transition: transform 0.3s ease;
#     }
    
#     .profile-img:hover {
#         transform: scale(1.05);
#     }
    
#     /* Typography */
#     .name-header {
#         font-size: 2.5rem;
#         font-weight: 700;
#         text-align: center;
#         margin: 1rem 0;
#     }
    
#     .title-text {
#         font-size: 1.25rem;
#         text-align: center;
#         margin-bottom: 0.5rem;
#     }
    
#     .company-text {
#         font-size: 1.1rem;
#         text-align: center;
#         margin-bottom: 1.5rem;
#     }
    
#     /* Contact Items */
#     .contact-item {
#         padding: 0.75rem 1rem;
#         margin: 0.5rem 0;
#         border-radius: 8px;
#         transition: transform 0.2s ease;
#     }
    
#     .contact-item:hover {
#         transform: translateX(10px);
#     }
    
#     .contact-item a {
#         text-decoration: none;
#     }
    
#     /* Social Links */
#     .social-links {
#         display: flex;
#         justify-content: center;
#         gap: 1rem;
#         margin: 1.5rem 0;
#     }
    
#     .social-links img {
#         transition: transform 0.2s ease;
#     }
    
#     .social-links img:hover {
#         transform: translateY(-3px);
#     }
    
#     /* Buttons */
#     .download-btn {
#         background-color: #4CAF50;
#         color: white;
#         padding: 0.75rem 1.5rem;
#         border-radius: 8px;
#         border: none;
#         cursor: pointer;
#         font-size: 1rem;
#         display: inline-flex;
#         align-items: center;
#         gap: 0.5rem;
#         transition: all 0.2s ease;
#     }
    
#     .download-btn:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#     }
    
#     /* Dark Mode */
#     @media (prefers-color-scheme: dark) {
#         .main-container {
#             background-color: #1a1a1a;
#             color: #ffffff;
#         }
#         .name-header {
#             color: #ffffff;
#         }
#         .title-text, .company-text {
#             color: #e5e7eb;
#         }
#         .contact-item {
#             background-color: #2d2d2d;
#         }
#         .contact-item a {
#             color: #e5e7eb;
#         }
#         .contact-item:hover {
#             background-color: #3d3d3d;
#         }
#         .download-btn {
#             background-color: #2563eb;
#         }
#         .download-btn:hover {
#             background-color: #1d4ed8;
#         }
#     }
    
#     /* Light Mode */
#     @media (prefers-color-scheme: light) {
#         .main-container {
#             background-color: #ffffff;
#             color: #1f2937;
#         }
#         .name-header {
#             color: #1f2937;
#         }
#         .title-text, .company-text {
#             color: #4b5563;
#         }
#         .contact-item {
#             background-color: #f3f4f6;
#         }
#         .contact-item a {
#             color: #4b5563;
#         }
#         .contact-item:hover {
#             background-color: #e5e7eb;
#         }
#     }import streamlit as st
# from PIL import Image
# import requests
# from io import BytesIO
# import base64
# import json
# </style>
# """, unsafe_allow_html=True)

# def fetch_user_data(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as err:
#         st.error(f"Error fetching user data: {err}")
#         return None

# if st.query_params.get("userId"):
#     user_id = st.query_params["userId"]
#     # st.write(f"User ID: {user_id}")
# else:
#     user_id = st.text_input("Enter User ID")


# # URL to fetch user data
# user_data_url = f"http://localhost:27017/user/businessCard/getInfo/{user_id}"


# # Fetch user data
# user_data = fetch_user_data(user_data_url)


# # Check if user data is available
# if user_data:


#     # Extract relevant information from user data
#     name = user_data.get("name", "")
#     title = user_data.get("designation", "sampleTitle")
#     company = user_data.get("company", "")
#     email = user_data.get("email", "")
#     phone = user_data.get("phone", "")
#     website = user_data.get("website", "")
#     location = user_data.get("location", "")
#     github = user_data.get("github", "")
#     linkedin = user_data.get("linkedin", "")
#     avatar_url = user_data.get("avatar_url", "")
    
#     print("user_data: ",user_data)
    
# if not user_data:
#     st.error("User data not found!")
#     st.stop()  # Stop execution if user data is invalid

# def get_avatar_image():
#     try:
#         response = requests.get(user_data["avatar_url"])
#         return BytesIO(response.content)
#     except:
#         return None

# # Main Layout
# with st.container():
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         # Profile Image with enhanced styling
#         avatar = get_avatar_image()
#         if avatar:
#             st.markdown(f"""
#                 <div style="text-align: center; margin: 2rem 0;">
#                     <img src="{user_data['avatar_url']}" 
#                          class="profile-img"
#                          alt="{user_data['name']}'s profile picture"
#                          width="150"
#                          height="150">
#                 </div>
#             """, unsafe_allow_html=True)

#         # Enhanced Name and Title section
#         st.markdown(f"""
#             <div style="text-align: center;">
#                 <h1 class="name-header">{user_data['name']}</h1>
#                 <div class="title-text">{user_data['title']}</div>
#                 <div class="company-text">{user_data['company']}</div>
#             </div>
#         """, unsafe_allow_html=True)

#         st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
        
#         # Contact Information with icons and hover effects
#         for item, icon in [
#             ('email', '📧'), ('phone', '📱'), ('website', '🌐'), ('location', '📍')
#         ]:
#             value = user_data[item]
#             href = f"mailto:{value}" if item == 'email' else \
#                    f"tel:{value}" if item == 'phone' else \
#                    f"https://{value}" if item == 'website' else "#"
            
#             st.markdown(f"""
#                 <div class="contact-item">
#                     {icon} <a href="{href}" target="_blank">{value}</a>
#                 </div>
#             """, unsafe_allow_html=True)

#         # Social Links with enhanced styling
#         st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
#         st.markdown(f"""
#             <div class="social-links">
#                 <a href="https://github.com/{user_data['github']}" target="_blank">
#                     <img src="https://img.shields.io/badge/GitHub-%2312100E.svg?&style=for-the-badge&logo=Github&logoColor=white" 
#                          alt="GitHub Profile"/>
#                 </a>
#                 <a href="https://www.linkedin.com/in/{user_data['linkedin']}" target="_blank">
#                     <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"
#                          alt="LinkedIn Profile"/>
#                 </a>
#             </div>
#         """, unsafe_allow_html=True)

#         # Save Contact Button with enhanced styling
#         if st.button("📱 Save Contact", key="save_contact"):
#             vcard = [
#                 "BEGIN:VCARD",
#                 "VERSION:2.1",
#                 f"N;CHARSET=UTF-8:{user_data['name'].split()[-1]};{' '.join(user_data['name'].split()[:-1])}",
#                 f"FN;CHARSET=UTF-8:{user_data['name']}",
#                 f"ORG;CHARSET=UTF-8:{user_data['company']}",
#                 f"TITLE;CHARSET=UTF-8:{user_data['title']}",
#                 f"TEL;CELL:{user_data['phone'].replace(' ', '').replace('+', '')}",
#                 f"EMAIL;INTERNET:{user_data['email']}",
#                 f"URL:{user_data['website']}",
#                 f"ADR;HOME;CHARSET=UTF-8:;;{user_data['location']}",
#                 "END:VCARD"
#             ]
            
#             vcard_text = "\r\n".join(vcard) + "\r\n"
#             b64_vcard = base64.b64encode(vcard_text.encode('utf-8')).decode()
            
#             st.markdown(f'''
#                 <div style="text-align: center; margin-top: 2rem;">
#                     <a href="data:text/x-vcard;charset=utf-8;base64,{b64_vcard}" 
#                        download="contact.vcf"
#                        class="download-btn">
#                         📥 Download Contact
#                     </a>
#                     <p style="margin-top: 1rem; color: #666; font-size: 0.875rem;">
#                         1. Click to download<br>
#                         2. Open the file<br>
#                         3. Add to contacts
#                     </p>
#                 </div>
#             ''', unsafe_allow_html=True)

















































import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import base64
import json

# Page configuration
st.set_page_config(
    page_title="Digital Visiting Card",
    page_icon="🪪",
    layout="centered"
)

# Enhanced Custom CSS with better color schemes and transitions
st.markdown("""
<style>
    /* Global Styles */
    * {
        transition: all 0.3s ease-in-out;
    }
    
    /* Main Container */
    .main-container {
        max-width: 800px;
        margin: auto;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Profile Image */
    .profile-img {
        border-radius: 50%;
        margin: auto;
        display: block;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .profile-img:hover {
        transform: scale(1.05);
    }
    
    /* Typography */
    .name-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
    }
    
    .title-text {
        font-size: 1.25rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .company-text {
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Contact Items */
    .contact-item {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        transition: transform 0.2s ease;
    }
    
    .contact-item:hover {
        transform: translateX(10px);
    }
    
    .contact-item a {
        text-decoration: none;
    }
    
    /* Social Links */
    .social-links {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .social-links img {
        transition: transform 0.2s ease;
    }
    
    .social-links img:hover {
        transform: translateY(-3px);
    }
    
    /* Buttons */
    .download-btn {
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 1rem;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Dark Mode */
    @media (prefers-color-scheme: dark) {
        .main-container {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        .name-header {
            color: #ffffff;
        }
        .title-text, .company-text {
            color: #e5e7eb;
        }
        .contact-item {
            background-color: #2d2d2d;
        }
        .contact-item a {
            color: #e5e7eb;
        }
        .contact-item:hover {
            background-color: #3d3d3d;
        }
        .download-btn {
            background-color: #2563eb;
        }
        .download-btn:hover {
            background-color: #1d4ed8;
        }
    }
    
    /* Light Mode */
    @media (prefers-color-scheme: light) {
        .main-container {
            background-color: #ffffff;
            color: #1f2937;
        }
        .name-header {
            color: #1f2937;
        }
        .title-text, .company-text {
            color: #4b5563;
        }
        .contact-item {
            background-color: #f3f4f6;
        }
        .contact-item a {
            color: #4b5563;
        }
        .contact-item:hover {
            background-color: #e5e7eb;
        }
    }
</style>
""", unsafe_allow_html=True)

def fetch_user_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        st.error(f"Error fetching user data: {err}")
        return None

if st.query_params.get("userId"):
    user_id = st.query_params["userId"]
else:
    user_id = st.text_input("Enter User ID")

# URL to fetch user data
user_data_url = f"http://localhost:27017/user/businessCard/getInfo/{user_id}"

# Fetch user data
user_data = fetch_user_data(user_data_url)

# Check if user data is available
if not user_data:
    st.error("User data not found!")
    st.stop()  # Stop execution if user data is invalid

def get_avatar_image():
    try:
        response = requests.get(user_data["avatar_url"])
        return BytesIO(response.content)
    except:
        return None

# Main Layout
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Profile Image with enhanced styling
        avatar = get_avatar_image()
        if avatar:
            st.markdown(f"""
                <div style="text-align: center; margin: 2rem 0;">
                    <img src="{user_data['avatar_url']}" 
                         class="profile-img"
                         alt="{user_data['name']}'s profile picture"
                         width="150"
                         height="150">
                </div>
            """, unsafe_allow_html=True)

        # Enhanced Name and Title section
        st.markdown(f"""
            <div style="text-align: center;">
                <h1 class="name-header">{user_data['name']}</h1>
                <div class="title-text">{user_data['designation']}</div>
                <div class="company-text">{user_data['organization']}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
        
        # Contact Information with icons and hover effects
        for item, icon in [
            ('email', '📧'), ('mobile', '📱'), ('website', '🌐'), ('location', '📍')
        ]:
            value = user_data.get(item, '')
            href = f"mailto:{value}" if item == 'email' else \
                   f"tel:{value}" if item == 'mobile' else \
                   f"https://{value}" if item == 'website' else "#"
            
            st.markdown(f"""
                <div class="contact-item">
                    {icon} <a href="{href}" target="_blank">{value}</a>
                </div>
            """, unsafe_allow_html=True)

        # About section
        if 'about' in user_data and user_data['about']:
            st.markdown(f"""
                <div class="contact-item">
                    📜 {user_data['about']}
                </div>
            """, unsafe_allow_html=True)

        # Social Links with enhanced styling
        st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="social-links">
                <a href="https://github.com/{user_data.get('github', '')}" target="_blank">
                    <img src="https://img.shields.io/badge/GitHub-%2312100E.svg?&style=for-the-badge&logo=Github&logoColor=white" 
                         alt="GitHub Profile"/>
                </a>
                <a href="https://www.linkedin.com/in/{user_data.get('linkedin', '')}" target="_blank">
                    <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"
                         alt="LinkedIn Profile"/>
                </a>
            </div>
        """, unsafe_allow_html=True)

        # Save Contact Button with enhanced styling
        if st.button("📱 Save Contact", key="save_contact"):
            vcard = [
                "BEGIN:VCARD",
                "VERSION:2.1",
                f"N;CHARSET=UTF-8:{user_data['name'].split()[-1]};{' '.join(user_data['name'].split()[:-1])}",
                f"FN;CHARSET=UTF-8:{user_data['name']}",
                f"ORG;CHARSET=UTF-8:{user_data['organization']}",
                f"TITLE;CHARSET=UTF-8:{user_data['designation']}",
                f"TEL;CELL:{user_data['mobile'].replace(' ', '').replace('+', '')}",
                f"EMAIL;INTERNET:{user_data['email']}",
                f"URL:{user_data['website']}",
                f"ADR;HOME;CHARSET=UTF-8:;;{user_data['location']}",
                "END:VCARD"
            ]
            
            vcard_text = "\r\n".join(vcard) + "\r\n"
            b64_vcard = base64.b64encode(vcard_text.encode('utf-8')).decode()
            
            st.markdown(f'''
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="data:text/x-vcard;charset=utf-8;base64,{b64_vcard}" 
                       download="contact.vcf"
                       class="download-btn">
                        📥 Download Contact
                    </a>
                    <p style="margin-top: 1rem; color: #666; font-size: 0.875rem;">
                        1. Click to download<br>
                        2. Open the file<br>
                        3. Add to contacts
                    </p>
                </div>
            ''', unsafe_allow_html=True)
