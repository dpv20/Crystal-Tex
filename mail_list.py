import os
import streamlit as st
import pandas as pd
from pathlib import Path
import json
import sqlite3
import uuid
import secrets
import string

def mail_list():
    file = 'mails.csv'
    st.title("mails")
    # Load data
    
    if not os.path.exists(file) or os.stat(file).st_size == 0:
        mails = pd.DataFrame(columns=['mails', 'type'])
    else:
        mails = pd.read_csv(file)
        if 'mails' not in mails.columns or 'type' not in mails.columns:
            mails = pd.DataFrame(columns=['mails', 'type'])

    st.markdown(mails.to_html(index=False), unsafe_allow_html=True)

    # Add email section
    st.write("## Add Email")
    new_mail = st.text_input("New Email")
    types = ['Operaciones', 'Arquitectura', 'Ingenieria', 'Otros']
    new_type = st.selectbox('Type', types)
    if st.button("Add Email"):
        if new_mail not in mails['mails'].values:
            mails = mails.append({'mails': new_mail, 'type': new_type}, ignore_index=True)
            mails.to_csv(file, index=False)
            st.success(f"Email {new_mail} added successfully.")
            st.experimental_rerun()
        else:
            st.error(f"Email {new_mail} is already in the list.")
    
    # Delete email section
    st.write("## Delete Email")
    delete_mail = st.text_input("Email to delete")
    if st.button("Delete Email"):
        if delete_mail in mails['mails'].values:
            mails = mails[mails.mails != delete_mail]
            mails.to_csv(file, index=False)
            st.success(f"Email {delete_mail} deleted successfully.")
            st.experimental_rerun()
        else:
            st.error(f"Email {delete_mail} not found.")
