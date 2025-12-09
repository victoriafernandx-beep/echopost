import streamlit as st
import time
from src import database

def init_session_state():
    """Initialize session state variables for auth"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'auth_checked' not in st.session_state:
        st.session_state.auth_checked = False

def get_current_user():
    """Get the currently logged in user"""
    if 'user' not in st.session_state:
        return None
    return st.session_state.user

def login(email, password):
    """Log in existin user"""
    supabase = database.init_supabase()
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.session_state.user = response.user
        return True, "Login realizado com sucesso!"
    except Exception as e:
        return False, f"Erro no login: {str(e)}"

def signup(email, password):
    """Sign up new user"""
    supabase = database.init_supabase()
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        # Check if email confirmation is required
        if response.user and response.user.identities and len(response.user.identities) > 0:
            return True, "Conta criada! Verifique seu email se necessário."
        else:
            # Sometimes signup returns user but maybe waits for confirm
            # If auto-confirm is on, we might be good
            if response.user:
                 st.session_state.user = response.user
                 return True, "Conta criada com sucesso!"
            return False, "Erro desconhecido ao criar conta."
    except Exception as e:
        return False, f"Erro no cadastro: {str(e)}"

def logout():
    """Log out current user"""
    supabase = database.init_supabase()
    try:
        supabase.auth.sign_out()
    except:
        pass
    
    st.session_state.user = None
    # Clear other session data
    keys_to_clear = ['linkedin_access_token', 'linkedin_token_expires_in']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
