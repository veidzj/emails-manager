from pathlib import Path
import streamlit as st
from utils import *

def home_page():
  st.markdown('# Email Manager')

  current_addressees = st.session_state.current_addressees
  current_title = st.session_state.current_title
  current_body = st.session_state.current_body

  addressees = st.text_input('Email addressees:', value=current_addressees)
  title = st.text_input('Email title:', value=current_title)
  body = st.text_area('Email body:', value=current_body, height=400)
  col1, _, col3 = st.columns(3)
  col1.button('Send email', use_container_width=True, on_click=send_email_home, args=(addressees, title, body))
  col3.button('Clear', use_container_width=True, on_click=clear_home)

  st.session_state.current_addressees = addressees
  st.session_state.current_title = title
  st.session_state.current_body = body

def clear_home():
  st.session_state.current_addressees = ''
  st.session_state.current_title = ''
  st.session_state.current_body = ''

def send_email_home(addressees, title, body):
  # user_email = st.secrets['USER_EMAIL']
  # app_password = st.secrets['APP_PASSWORD']
  addressees = addressees.replace(' ', '').split(',')
  user_email = read_email()
  app_password = read_email_key()
  if user_email == '':
    st.error('Add your email in the settings page')
  elif app_password == '':
    st.error('Add your email key in the settings page')
  else:
    send_email(user_email, addressees, title, body, app_password)

def email_list_page():
  st.markdown('# Email List')
  st.divider()

  for file in email_list_folder.glob('*.txt'):
    file_name = file.stem.replace('_', ' ').upper()
    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
    col1.button(file_name, key=f'{file_name}', use_container_width=True, on_click=use_list, args=(file_name,))
    col2.button('EDIT', key=f'edit_{file_name}', use_container_width=True, on_click=edit_list, args=(file_name,))
    col3.button('DELETE', key=f'delete_{file_name}', use_container_width=True, on_click=delete_list, args=(file_name,))

  st.divider()
  st.button('Add List', on_click=change_page, args=('add_list',))

def add_list_page(list_name='', list_emails=''):
  list_name = st.text_input('List name:', value=list_name)
  list_emails = st.text_area('Write the emails separated by commas:', value=list_emails, height=600)
  st.button('Save', on_click=save_list, args=(list_name, list_emails))

def use_list(name):
  file_name = name.replace(' ', '_').lower() + '.txt'
  with open(email_list_folder / file_name) as file:
      file_text = file.read()
  st.session_state.current_addressees = file_text
  change_page('home')

def save_list(name, text):
  email_list_folder.mkdir(exist_ok=True)
  file_name = name.replace(' ', '_').lower() + '.txt'
  with open(email_list_folder / file_name, 'w', encoding='utf-8') as file:
    file.write(text)
  change_page('email_list')

def delete_list(name):
  file_name = name.replace(' ', '_').lower() + '.txt'
  (email_list_folder / file_name).unlink()

def edit_list(name):
  file_name = name.replace(' ', '_').lower() + '.txt'
  with open(email_list_folder / file_name) as file:
    file_text = file.read()
  st.session_state.list_name_edit = name
  st.session_state.list_text_edit = file_text
  change_page('edit_list')

def settings_page():
  st.markdown('# Settings')

  email = st.text_input('Write your email:')
  st.button('Save', key='save_email', on_click=save_email, args=(email,))
  key = st.text_input('Write your email key:')
  st.button('Save', key='save_keyl', on_click=save_email_key, args=(key,))

def save_email(email):
  settings_folder.mkdir(exist_ok=True)
  with open(settings_folder / 'user_email.txt', 'w') as file:
    file.write(email)

def save_email_key(key):
  settings_folder.mkdir(exist_ok=True)
  with open(settings_folder / 'user_email_key.txt', 'w') as file:
    file.write(key)

def read_email():
  settings_folder.mkdir(exist_ok=True)
  if (settings_folder / 'user_email.txt').exists():
    with open(settings_folder / 'user_email_key.txt', 'r') as file:
      return file.read()
  return ''

def read_email_key():
  settings_folder.mkdir(exist_ok=True)
  if (settings_folder / 'user_email_key.txt').exists():
    with open(settings_folder / 'user_email_key.txt', 'r') as file:
      return file.read()
  return ''

def main():
  init()

  st.sidebar.button('Email Manager', use_container_width=True, on_click=change_page, args=('home',))
  st.sidebar.button('Templates', use_container_width=True, on_click=change_page, args=('templates',))
  st.sidebar.button('Email List', use_container_width=True, on_click=change_page, args=('email_list',))
  st.sidebar.button('Settings', use_container_width=True, on_click=change_page, args=('settings',))

  if st.session_state.email_manager_page == 'home':
    home_page()
  elif st.session_state.email_manager_page == 'templates':
    templates_page()
  elif st.session_state.email_manager_page == 'add_template':
    add_template_page()
  elif st.session_state.email_manager_page == 'edit_template':
    template_name_edit = st.session_state.template_name_edit
    template_text_edit = st.session_state.template_text_edit
    add_template_page(template_name_edit, template_text_edit)
  elif st.session_state.email_manager_page == 'email_list':
    email_list_page()
  elif st.session_state.email_manager_page == 'add_list':
    add_list_page()
  elif st.session_state.email_manager_page == 'edit_list':
    list_name_edit = st.session_state.list_name_edit
    list_text_edit = st.session_state.list_text_edit
    add_list_page(list_name_edit, list_text_edit)
  elif st.session_state.email_manager_page == 'settings':
    settings_page()

main()
