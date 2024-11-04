import streamlit as st
import os

st.title('About Us')

cwd = os.getcwd()
f = open(f"{cwd}/app/pages/about_us.md", "r")
content = f.read()

st.markdown(content)