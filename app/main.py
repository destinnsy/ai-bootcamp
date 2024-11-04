__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from helper.utility import check_password

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

st.title("AI Bootcamp Project Type A POC")

with st.expander("See Disclaimer!!!", True):
    st.write("""

IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

Always consult with qualified professionals for accurate and personalized advice.

""")