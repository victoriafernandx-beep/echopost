"""
LinkedIn Integration with OAuth 2.0
Real integration with LinkedIn API for posting and analytics
"""
import streamlit as st
import requests
from urllib.parse import urlencode

# LinkedIn OAuth endpoints
LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_API_BASE = "https://api.linkedin.com/v2"

def get_linkedin_credentials():
    """Get LinkedIn credentials from secrets"""
    try:
        return {
            "client_id": st.secrets.get("LINKEDIN_CLIENT_ID", ""),
            "client_secret": st.secrets.get("LINKEDIN_CLIENT_SECRET", ""),
            "redirect_uri": st.secrets.get("LINKEDIN_REDIRECT_URI", "https://seu-app.streamlit.app")
        }
    except Exception as e:
        print(f"Error loading LinkedIn credentials: {e}")
        return {
            "client_id": "",
            "client_secret": "",
            "redirect_uri": "https://seu-app.streamlit.app"
        }

def is_connected():
    """Check if user is connected to LinkedIn"""
    return 'linkedin_access_token' in st.session_state and st.session_state['linkedin_access_token'] is not None

def get_authorization_url():
    """Generate LinkedIn OAuth authorization URL"""
    creds = get_linkedin_credentials()
    
    if not creds['client_id']:
        return None
    
    params = {
        'response_type': 'code',
        'client_id': creds['client_id'],
        'redirect_uri': creds['redirect_uri'],
        'scope': 'openid profile email w_member_social'
    }
    
    return f"{LINKEDIN_AUTH_URL}?{urlencode(params)}"

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    creds = get_linkedin_credentials()
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': creds['redirect_uri'],
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret']
    }
    
    try:
        response = requests.post(LINKEDIN_TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()
        
        # Store token in session
        st.session_state['linkedin_access_token'] = token_data['access_token']
        st.session_state['linkedin_token_expires_in'] = token_data.get('expires_in', 5184000)
        
        # Save token to database for offline access
        from src import database, auth
        user = auth.get_current_user()
        
        if not user:
            return False, "❌ Erro de Sessão: Usuário não identificado ao conectar. Tente fazer login novamente."
            
        save_result = database.save_linkedin_token(
            user_id=user.id,
            access_token=token_data['access_token'],
            refresh_token=token_data.get('refresh_token'),
            expires_in=token_data.get('expires_in')
        )
        
        if not save_result:
            return False, "Erro crítico: Falha ao salvar token no banco de dados. Verifique os logs."
    
        return True, f"Conectado com sucesso! (ID: {user.id})"
    except Exception as e:
        return False, f"Erro ao conectar: {str(e)}"

def connect_linkedin():
    """Initiate LinkedIn OAuth flow"""
    creds = get_linkedin_credentials()
    
    if not creds['client_id'] or not creds['client_secret']:
        return False, "⚠️ Credenciais do LinkedIn não configuradas. Adicione LINKEDIN_CLIENT_ID e LINKEDIN_CLIENT_SECRET nos secrets."
    
    auth_url = get_authorization_url()
    if auth_url:
        return True, f"Clique aqui para conectar: {auth_url}"
    else:
        return False, "Erro ao gerar URL de autorização"

def disconnect_linkedin():
    """Disconnect from LinkedIn"""
    if 'linkedin_access_token' in st.session_state:
        del st.session_state['linkedin_access_token']
    if 'linkedin_token_expires_in' in st.session_state:
        del st.session_state['linkedin_token_expires_in']
    return True, "Desconectado do LinkedIn"

def get_user_profile():
    """Get LinkedIn user profile using OpenID Connect"""
    if not is_connected():
        return None
    
    headers = {
        'Authorization': f"Bearer {st.session_state['linkedin_access_token']}",
    }
    
    try:
        # Use OIDC userinfo endpoint
        response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Map OIDC fields to our expected format
        return {
            "id": data.get("sub"),
            "name": data.get("name"),
            "email": data.get("email"),
            "picture": data.get("picture")
        }
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None

def post_to_linkedin(content):
    """Post content to LinkedIn"""
    if not is_connected():
        return False, "Não conectado ao LinkedIn"
    
    # Get user profile first
    profile = get_user_profile()
    if not profile:
        return False, "Erro ao obter perfil do usuário"
    
    user_id = profile.get('id')
    
    # Prepare post data
    post_data = {
        "author": f"urn:li:person:{user_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    headers = {
        'Authorization': f"Bearer {st.session_state['linkedin_access_token']}",
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    try:
        response = requests.post(
            f"{LINKEDIN_API_BASE}/ugcPosts",
            headers=headers,
            json=post_data
        )
        response.raise_for_status()
        return True, "✅ Post publicado no LinkedIn com sucesso!"
    except requests.exceptions.HTTPError as e:
        error_msg = e.response.json() if e.response else str(e)
        return False, f"❌ Erro ao publicar: {error_msg}"
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"

def get_linkedin_metrics():
    """Get LinkedIn analytics (requires Marketing Developer Platform access)"""
    if not is_connected():
        return {
            "followers": 0,
            "impressions": 0,
            "engagement": 0,
            "error": "Não conectado"
        }
    
    # Note: This requires Marketing Developer Platform approval
    # For now, return mock data with a note
    return {
        "followers": 15230,
        "impressions": 45000,
        "engagement": 4.8,
        "note": "Métricas reais requerem aprovação do Marketing Developer Platform"
    }
