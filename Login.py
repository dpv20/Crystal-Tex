import os
import sys
import streamlit as st
import pandas as pd
from pathlib import Path
import json
import sqlite3
import uuid

from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import _on_pages_changed, get_pages
import streamlit.components.v1 as components



DEFAULT_PAGE = "Login.py"

st.set_page_config(page_title="Multipage App", page_icon=":key:")


from functions_webpage import *
from homepage import *
from surveys import *
from stages import *
from proyectos import *
from proyectos_pendientes2 import *  
from user_projects import *
from visitas import *
from send_mail import *
from mail_list import *
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    


# Initialize session state attributes
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = ""

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = ""

DEFAULT_PAGE = "Login.py"


# Set the theme to "dark"
#st.markdown("<h2 style='text-align: center; color: #C059C0;'> Welcome!</h2>", unsafe_allow_html=True)
st.write('-----')


clear_all_but_first_page()


users = load_users("users.csv")
df = pd.read_csv("users.csv")

def main():

    st.markdown(
        """
        <style>
            div[data-testid='stRadio'] div[class^='Widget'] label {
                font-size: 20px;  # Change the value as needed
            }
        </style>
        """,
        unsafe_allow_html=True,
    )



    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.sidebar.title('Menu')
        menu_options = ["homepage", "TEX"]
        if st.session_state['user_role'] == 'admin':
            menu_options.extend(["configuraciones", "Proyectos","Field Visit Form"])  
        if st.session_state['user_role'] != 'admin':
            menu_options.append("Mis proyectos")
        choice = st.sidebar.selectbox("Menu", menu_options)
        


        if choice == "Mis proyectos":
            Mis_proyectos(st.session_state['username'])

        if choice == "homepage":
            if st.session_state['logged_in']:
                homepage()
            else:
                login_page()

                
        elif choice == "TEX":
            tex_choice = st.sidebar.radio('Choose an option', ['Entire Project', 'Stages'])
            if tex_choice == 'Entire Project':
                surveys(st.session_state['username'])
            else:  # tex_choice == 'Stages'
                stages(st.session_state['username'])
        
        
        elif choice == "configuraciones":
            if st.session_state['user_role'] == 'admin':
                admin_choice = st.sidebar.radio('Choose an option', ['Crear nuevo usuario', 'listado de usuarios','listado de mails'])
                if admin_choice == 'Crear nuevo usuario':
                    nuevo_usuario()
                elif admin_choice == 'listado de usuarios':
                    display_users(users, 'users.csv')
                elif admin_choice == 'listado de mails':
                    mail_list()
            else:
                st.warning("Access denied. Only admin users can access this page.")
        
        

        elif choice == "Proyectos":
            if st.session_state['user_role'] == 'admin':
                proyects_choice = st.sidebar.radio('Choose an option', ['Proyectos por aprobar', 'Listado de Proyectos'])
                if proyects_choice == 'Proyectos por aprobar':
                    proyectos_pendientes()
                else:
                    proyectos()
            else:
                st.warning("Access denied. Only admin users can access this page.")



        elif choice == "Field Visit Form":
            field_visit_form()
    else:
        login_page()





if __name__ == "__main__":
    main()
