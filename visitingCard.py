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
    
#     /* Avatar Container */
#     .avatar-container {
#         width: 150px;
#         height: 150px;
#         margin: 2rem auto;
#         border-radius: 50%;
#         overflow: hidden;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#         transition: transform 0.3s ease;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 3rem;
#         font-weight: bold;
#         color: white;
#     }
    
#     .avatar-container:hover {
#         transform: scale(1.05);
#     }
    
#     .avatar-initials {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         width: 100%;
#         height: 100%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
    
#     /* Profile Image */
#     .profile-img {
#         width: 100%;
#         height: 100%;
#         object-fit: cover;
#     }
    
#     /* Typography */
#     .name-header {
#         font-size: 2.5rem;
#         font-weight: 700;
#         text-align: center;
#         margin: 1rem 0;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }
    
#     .title-text {
#         font-size: 1.25rem;
#         text-align: center;
#         margin-bottom: 0.5rem;
#         font-weight: 500;
#     }
    
#     .company-text {
#         font-size: 1.1rem;
#         text-align: center;
#         margin-bottom: 1.5rem;
#         opacity: 0.8;
#     }
    
#     /* Contact Items */
#     .contact-item {
#         padding: 1rem 1.5rem;
#         margin: 0.75rem 0;
#         border-radius: 12px;
#         transition: all 0.2s ease;
#         display: flex;
#         align-items: center;
#         gap: 1rem;
#     }
    
#     .contact-item:hover {
#         transform: translateX(10px);
#         box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
#     }
    
#     .contact-item a {
#         text-decoration: none;
#         flex-grow: 1;
#     }
    
#     /* Social Links */
#     .social-links {
#         display: flex;
#         justify-content: center;
#         gap: 1.5rem;
#         margin: 2rem 0;
#     }
    
#     .social-links img {
#         transition: transform 0.3s ease;
#         border-radius: 8px;
#     }
    
#     .social-links img:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#     }
    
#     /* Buttons */
#     .download-btn {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 1rem 2rem;
#         border-radius: 12px;
#         border: none;
#         cursor: pointer;
#         font-size: 1rem;
#         display: inline-flex;
#         align-items: center;
#         gap: 0.75rem;
#         transition: all 0.3s ease;
#         text-decoration: none;
#     }
    
#     .download-btn:hover {
#         transform: translateY(-3px);
#         box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.2);
#     }
    
#     /* Dark Mode */
#     @media (prefers-color-scheme: dark) {
#         .main-container {
#             background-color: #1a1a1a;
#             color: #ffffff;
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
#     }
    
#     /* Light Mode */
#     @media (prefers-color-scheme: light) {
#         .main-container {
#             background-color: #ffffff;
#             color: #1f2937;
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
#     }
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

# def get_initials(name):
#     return ''.join(word[0].upper() for word in name.split() if word)

# if st.query_params.get("userId"):
#     user_id = st.query_params["userId"]
# else:
#     user_id = st.text_input("Enter User ID")

# # URL to fetch user data
# user_data_url = f"http://localhost:27017/user/businessCard/getInfo/{user_id}"

# # Fetch user data
# user_data = fetch_user_data(user_data_url)

# # Check if user data is available
# if not user_data:
#     st.error("User data not found!")
#     st.stop()

# # Main Layout
# with st.container():
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         # Avatar or Initials
#         has_avatar = 'avatar_url' in user_data and user_data['avatar_url']
#         if has_avatar:
#             st.markdown(f"""
#                 <div class="avatar-container">
#                     <img src="{user_data['avatar_url']}" 
#                          class="profile-img"
#                          alt="{user_data['name']}'s profile picture">
#                 </div>
#             """, unsafe_allow_html=True)
#         else:
#             initials = get_initials(user_data['name'])
#             st.markdown(f"""
#                 <div class="avatar-container">
#                     <div class="avatar-initials">{initials}</div>
#                 </div>
#             """, unsafe_allow_html=True)

#         # Enhanced Name and Title section
#         st.markdown(f"""
#             <div style="text-align: center;">
#                 <h1 class="name-header">{user_data['name']}</h1>
#                 <div class="title-text">{user_data['designation']}</div>
#                 <div class="company-text">{user_data['organization']}</div>
#             </div>
#         """, unsafe_allow_html=True)

#         st.markdown("<hr style='margin: 2rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        
#         # Contact Information with icons and hover effects
#         contact_icons = {
#             'email': '📧',
#             'mobile': '📱',
#             'location': '📍',
#             'website': '🌐'
#         }
        
#         for item, icon in contact_icons.items():
#             if item in user_data and user_data[item]:
#                 value = user_data[item]
#                 href = f"mailto:{value}" if item == 'email' else \
#                        f"tel:{value}" if item == 'mobile' else \
#                        f"https://{value}" if item == 'website' else "#"
                
#                 st.markdown(f"""
#                     <div class="contact-item">
#                         <span style="font-size: 1.5rem;">{icon}</span>
#                         <a href="{href}" target="_blank">{value}</a>
#                     </div>
#                 """, unsafe_allow_html=True)

#         # About section with enhanced styling
#         if 'about' in user_data and user_data['about']:
#             st.markdown(f"""
#                 <div class="contact-item" style="background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);">
#                     <span style="font-size: 1.5rem;">📜</span>
#                     <div style="flex-grow: 1;">{user_data['about']}</div>
#                 </div>
#             """, unsafe_allow_html=True)

#         # Social Links with enhanced styling
#         if any(key in user_data for key in ['github', 'linkedin']):
#             st.markdown("<hr style='margin: 2rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
#             social_links = []
            
#             if 'github' in user_data and user_data['github']:
#                 social_links.append(f"""
#                     <a href="https://github.com/{user_data['github']}" target="_blank">
#                         <img src="https://img.shields.io/badge/GitHub-%2312100E.svg?&style=for-the-badge&logo=Github&logoColor=white" 
#                              alt="GitHub Profile"/>
#                     </a>
#                 """)
            
#             if 'linkedin' in user_data and user_data['linkedin']:
#                 social_links.append(f"""
#                     <a href="https://www.linkedin.com/in/{user_data['linkedin']}" target="_blank">
#                         <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"
#                              alt="LinkedIn Profile"/>
#                     </a>
#                 """)
            
#             if social_links:
#                 st.markdown(f"""
#                     <div class="social-links">
#                         {"".join(social_links)}
#                     </div>
#                 """, unsafe_allow_html=True)

#         # Save Contact Button with enhanced styling
#         if st.button("📱 Save Contact", key="save_contact"):
#             vcard = [
#                 "BEGIN:VCARD",
#                 "VERSION:2.1",
#                 f"N;CHARSET=UTF-8:{user_data['name'].split()[-1]};{' '.join(user_data['name'].split()[:-1])}",
#                 f"FN;CHARSET=UTF-8:{user_data['name']}",
#                 f"ORG;CHARSET=UTF-8:{user_data['organization']}",
#                 f"TITLE;CHARSET=UTF-8:{user_data['designation']}",
#                 f"TEL;CELL:{user_data.get('mobile', '').replace(' ', '').replace('+', '')}",
#                 f"EMAIL;INTERNET:{user_data.get('email', '')}",
#                 f"URL:{user_data.get('website', '')}",
#                 f"ADR;HOME;CHARSET=UTF-8:;;{user_data.get('location', '')}",
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
#                     <p style="margin-top: 1.5rem; color: #666; font-size: 0.9rem;">
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
import streamlit.components.v1 as components

# Page configuration with improved title and icon
st.set_page_config(
    page_title="✨ Digital Business Card",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Modern Custom CSS with glassmorphism effects and animations
st.markdown("""
<style>
    /* Global Styles */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Inter', sans-serif;
    }
    
    /* Glassmorphism Card Container */
    .main-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2.5rem;
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 0 0 1px rgba(255, 255, 255, 0.5);
    }
    
    /* Enhanced Avatar Container */
    .avatar-container {
        width: 180px;
        height: 180px;
        margin: 2rem auto;
        border-radius: 50%;
        overflow: hidden;
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.2),
            0 0 0 2px rgba(255, 255, 255, 0.9);
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .avatar-container:hover {
        transform: scale(1.05) translateY(-5px);
    }
    
    .avatar-initials {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Enhanced Typography */
    .name-header {
        font-size: 2.75rem;
        font-weight: 800;
        text-align: center;
        margin: 1.5rem 0;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    
    .title-text {
        font-size: 1.4rem;
        text-align: center;
        margin-bottom: 0.75rem;
        font-weight: 600;
        color: #4b5563;
    }
    
    .company-text {
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Modern Contact Items */
    .contact-item {
        padding: 1.25rem 1.75rem;
        margin: 1rem 0;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(229, 231, 235, 0.5);
        display: flex;
        align-items: center;
        gap: 1.25rem;
    }
    
    .contact-item:hover {
        transform: translateX(10px) translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        background: rgba(255, 255, 255, 0.95);
    }
    
    .contact-item a {
        text-decoration: none;
        color: #4b5563;
        font-weight: 500;
        flex-grow: 1;
    }
    
    .contact-item a:hover {
        color: #6366f1;
    }
    
    /* Enhanced Social Links */
    .social-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2.5rem 0;
    }
    
    .social-links img {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 8px;
        filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
    }
    
    .social-links img:hover {
        transform: translateY(-5px);
        filter: drop-shadow(0 8px 12px rgba(0, 0, 0, 0.15));
    }
    
    /* Modern Download Button */
    .download-btn {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        padding: 1.25rem 2.5rem;
        border-radius: 16px;
        border: none;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 1rem;
        text-decoration: none;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    .download-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    /* Enhanced Dark Mode */
    @media (prefers-color-scheme: dark) {
        .main-container {
            background: rgba(17, 24, 39, 0.95);
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.2),
                inset 0 0 0 1px rgba(255, 255, 255, 0.1);
        }
        .contact-item {
            background: rgba(31, 41, 55, 0.8);
            border-color: rgba(75, 85, 99, 0.2);
        }
        .contact-item a {
            color: #e5e7eb;
        }
        .contact-item:hover {
            background: rgba(31, 41, 55, 0.95);
        }
        .title-text {
            color: #d1d5db;
        }
        .company-text {
            color: #9ca3af;
        }
    }
</style>
""", unsafe_allow_html=True)

def fetch_user_data(url):
    """Fetch user data with improved error handling."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        st.error(f"⚠️ Error fetching user data: {err}")
        return None

def get_initials(name):
    """Get initials with improved handling of empty strings."""
    if not name:
        return "👤"
    return ''.join(word[0].upper() for word in name.split() if word)

# Input userId with improved UI
user_id = st.query_params.get("userId")
if not user_id:
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #6366f1; font-size: 2rem; margin-bottom: 1rem;'>🪪 Digital Business Card</h1>
        </div>
    """, unsafe_allow_html=True)
    user_id = st.text_input("Enter User ID", placeholder="Type your user ID here...")

# URL to fetch user data
# user_data_url = f"http://localhost:27017/user/businessCard/getInfo/{user_id}"

user_data_url = f"https://gatherhub-r7yr.onrender.com/user/businessCard/getInfo/{user_id}"


# Fetch user data with loading state
if user_id:
    with st.spinner("Loading business card..."):
        user_data = fetch_user_data(user_data_url)
else:
    user_data = None

# If user data is unavailable, show enhanced error message
if not user_data and user_id:
    st.error("👻 User data not found! Please check the User ID and try again.")
    st.stop()

# Main Layout with enhanced structure
if user_data:
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Enhanced Avatar or Initials
            has_avatar = 'avatar_url' in user_data and user_data['avatar_url']
            if has_avatar:
                st.markdown(f"""
                    <div class="avatar-container">
                        <img src="{user_data['avatar_url']}" 
                             class="profile-img"
                             alt="{user_data['name']}'s profile picture"
                             loading="lazy">
                    </div>
                """, unsafe_allow_html=True)
            else:
                initials = get_initials(user_data['name'])
                st.markdown(f"""
                    <div class="avatar-container">
                        <div class="avatar-initials">{initials}</div>
                    </div>
                """, unsafe_allow_html=True)

            # Enhanced Name and Title section
            st.markdown(f"""
                <div style="text-align: center;">
                    <h1 class="name-header">{user_data['name']}</h1>
                    <div class="title-text">{user_data.get('designation', 'Professional')}</div>
                    <div class="company-text">{user_data.get('organization', '')}</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<hr style='margin: 2rem 0; opacity: 0.1;'>", unsafe_allow_html=True)
            
            # Enhanced Contact Information with modern icons
            contact_icons = {
                'email': '✉️',
                'mobile': '📱',
                'location': '📍',
                # 'website': '🌐'
            }
            
            for item, icon in contact_icons.items():
                if item in user_data and user_data[item]:
                    value = user_data[item]
                    href = f"mailto:{value}" if item == 'email' else f"tel:{value}" if item == 'mobile' else "#"
                    
                    st.markdown(f"""
                        <div class="contact-item">
                            <span style="font-size: 1.5rem;">{icon}</span>
                            <a href="{href}" target="_blank">{value}</a>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Enhanced Social Media Links
            st.markdown("<hr style='margin: 2rem 0; opacity: 0.1;'>", unsafe_allow_html=True)
            
            social_icons = {
                'linkedin': "https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"
            }

            # Explicit LinkedIn handling
            linkedin_url = user_data.get('linkedIn', '')
            
            if linkedin_url:
                # Ensure URL starts with https://
                if not linkedin_url.startswith(('http://', 'https://')):
                    linkedin_url = f"https://{linkedin_url}"
                
                st.markdown(f"""
                    <div class="social-links">
                        <a href="{linkedin_url}" target="_blank" rel="noopener noreferrer">
                            <img src="{social_icons['linkedin']}" alt="LinkedIn Profile" />
                        </a>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align: center; color: #6b7280; padding: 1rem;">
                        No LinkedIn profile available
                    </div>
                """, unsafe_allow_html=True)


            # Enhanced Download Button
             # Save Contact Button with enhanced styling
        if st.button("📱 Save Contact", key="save_contact"):
            vcard = [
                "BEGIN:VCARD",
                "VERSION:2.1",
                f"N;CHARSET=UTF-8:{user_data['name'].split()[-1]};{' '.join(user_data['name'].split()[:-1])}",
                f"FN;CHARSET=UTF-8:{user_data['name']}",
                f"ORG;CHARSET=UTF-8:{user_data['organization']}",
                f"TITLE;CHARSET=UTF-8:{user_data['designation']}",
                f"TEL;CELL:{user_data.get('mobile', '').replace(' ', '').replace('+', '')}",
                f"EMAIL;INTERNET:{user_data.get('email', '')}",
                f"URL:{user_data.get('website', '')}",
                f"ADR;HOME;CHARSET=UTF-8:;;{user_data.get('location', '')}",
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
                    <p style="margin-top: 1.5rem; color: #666; font-size: 0.9rem;">
                        1. Click to download<br>
                        2. Open the file<br>
                        3. Add to contacts
                    </p>
                </div>
            ''', unsafe_allow_html=True)