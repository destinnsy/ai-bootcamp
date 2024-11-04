import streamlit as st
import os
from helper.utility import check_password

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

st.title('About Us')

cwd = os.getcwd()
f = open(f"{cwd}/app/pages/about_us.md", "r")
content = f.read()

st.markdown(content)