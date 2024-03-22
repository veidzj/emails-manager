from pathlib import Path
import streamlit as st

current_folder = Path(__file__).parent
templates_foler = current_folder / 'templates'
email_list_folder = current_folder / 'email_list'

if not 'email_manager_page' in st.session_state:
  st.session_state.email_manager_page = 'home'

def change_page(page_name: str):
  st.session_state.email_manager_page = page_name

def home_page():
  st.markdown('# Email Manager')

def templates_page():
  st.markdown('# Templates')

  st.button('Add template', on_click=change_page, args=('add_template',))

def add_template_page():
  template_name = st.text_input('Template name:')
  template_text = st.text_area('Write the template text:', height=600)
  st.button('Save', on_click=save_template, args=(template_name, template_text))

def save_template(name, text):
  templates_foler.mkdir(exist_ok=True)
  file_name = name.replace(' ', '_').lower() + '.txt'
  with open(templates_foler / file_name, 'w', encoding='utf-8') as file:
    file.write(text)
  change_page('templates')

def email_list_page():
  st.markdown('# Email List')

  st.button('Add List', on_click=change_page, args=('add_list',))

def add_list_page():
  list_name = st.text_input('List name:')
  list_emails = st.text_area('Write the emails separated by commas:', height=600)
  st.button('Save', on_click=save_list, args=(list_name, list_emails))

def save_list(name, text):
  email_list_folder.mkdir(exist_ok=True)
  file_name = name.replace(' ', '_').lower() + '.txt'
  with open(email_list_folder / file_name, 'w', encoding='utf-8') as file:
    file.write(text)
  change_page('email_list')

def settings_page():
  st.markdown('# Settings')



def main():
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
  elif st.session_state.email_manager_page == 'email_list':
    email_list_page()
  elif st.session_state.email_manager_page == 'add_list':
    add_list_page()
  elif st.session_state.email_manager_page == 'settings':
    settings_page()

main()
