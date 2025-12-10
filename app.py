import streamlit as st
from src import database
from src import generator
import datetime

# Handle OAuth callback
if "code" in st.query_params:
    code = st.query_params["code"]
    from src import linkedin
    success, message = linkedin.exchange_code_for_token(code)
    if success:
        st.success("✅ LinkedIn conectado com sucesso!")
        # Clear query params to avoid re-execution
        st.query_params.clear()
    else:
        st.error(f"❌ Erro ao conectar: {message}")

st.set_page_config(
    page_title="LinPost - Conteúdo Inteligente para LinkedIn",
    page_icon="assets/logo-icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# AUTHENTICATION
# ============================================
from src import auth

# Initialize auth state
auth.init_session_state()
user = auth.get_current_user()

if not user:
    # Sidebar logo
    st.sidebar.image("assets/logo.png", width=200)
    st.sidebar.markdown("---")
    
    # Login/Signup UI
    st.title("🔐 Login no LinPost")
    
    tab_login, tab_signup = st.tabs(["Entrar", "Criar Conta"])
    
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar", type="primary", use_container_width=True)
            
            if submitted:
                success, msg = auth.login(email, password)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    with tab_signup:
        with st.form("signup_form"):
            email_new = st.text_input("Email")
            pass_new = st.text_input("Senha", type="password")
            submitted_new = st.form_submit_button("Criar Conta", use_container_width=True)
            
            if submitted_new:
                success, msg = auth.signup(email_new, pass_new)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
    
    st.info("💡 Dica: Se você acabou de configurar o Supabase, certifique-se que o provider 'Email' está habilitado.")
    st.stop()  # Stop execution here if not logged in

# Logout button in sidebar (bottom)
with st.sidebar:
    st.markdown("---")
    st.write(f"👤 {user.email}")
    if st.button("Sair", use_container_width=True):
        auth.logout()
        st.rerun()

# Initialize scheduler for automatic post publishing
try:
    from src import scheduler
    if 'scheduler_started' not in st.session_state:
        scheduler.start_scheduler()
        st.session_state['scheduler_started'] = True
except Exception as e:
    # Silently fail if scheduler can't start (e.g., missing dependencies)
    pass

# LinPost Premium Theme - New Brand Identity
# LinPost Professional Blue Theme - New Corporate Identity
current_theme = {
    # Primary Colors
    "purple_neon": "#0077B5",      # Brand identity (Blue Corporate) - kept key name for compatibility
    "cyan_blue": "#0077B5",        # Primary actions (Blue Corporate)
    "deep_black": "#2C3E50",       # Main text (Navy Blue)
    
    # Secondary Colors
    "soft_gray": "#F4F6F9",        # Background (Light Gray)
    "graphite": "#2C3E50",         # Text (Navy Blue)
    "border_gray": "#E5E7EB",      # Borders
    "light_lilac": "#00BCD4",      # Highlight (Cyan Light) - kept key name compatibility
    "light_blue": "#E1F5FE",       # Hover states
    
    # Feedback Colors
    "success": "#00A36C",          # Green
    "warning": "#FFC107",          # Yellow
    "error": "#E74C3C",            # Red
    
    # Backgrounds
    "bg_main": "#F4F6F9",
    "bg_sidebar": "#FFFFFF",
    "card_bg": "#FFFFFF"
}

st.markdown(f"""
<style>
    /* LinPost Mobile-First Design System v2.0 */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    /* === GLOBAL CANVAS === */
    .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(180deg, #E1F5FE 0%, #F0F9FF 30%, #FFFFFF 100%);
        background-attachment: fixed;
    }}
    
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 800px !important; /* Mobile app feel width */
    }}
    
    /* === TYPOGRAPHY === */
    h1, h2, h3 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: {current_theme['deep_black']} !important;
    }}
    
    h1 {{
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(90deg, #0077B5 0%, #00A0DC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    h2 {{
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 0.75rem !important;
    }}
    
    h3 {{
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }}
    
    /* === SIDEBAR (Modern & Minimal) === */
    section[data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(229, 231, 235, 0.5);
    }}
    
    /* Hide default radio buttons */
    section[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-of-type,
    section[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-of-type {{
        display: none !important;
    }}
    
    /* Sidebar Navigation Items */
    section[data-testid="stSidebar"] [role="radiogroup"] > label {{
        background: transparent !important;
        color: {current_theme['graphite']} !important;
        font-weight: 500 !important;
        padding: 0.875rem 1rem !important;
        margin: 0.25rem 0.5rem !important;
        border-radius: 12px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid transparent !important;
    }}
    
    /* Sidebar Hover */
    section[data-testid="stSidebar"] [role="radiogroup"] > label:hover {{
        background-color: #F8FAFC !important;
        color: {current_theme['purple_neon']} !important;
        transform: translateX(4px);
    }}

    /* Sidebar Active */
    section[data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"],
    section[data-testid="stSidebar"] [role="radiogroup"] > label[data-checked="true"] {{
        background-color: #E1F5FE !important;
        color: {current_theme['purple_neon']} !important;
        font-weight: 700 !important;
        border: 1px solid {current_theme['purple_neon']}20 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 119, 181, 0.1) !important;
    }}
    
    /* === CARDS (Soft Shadow & 16px Radius) === */
    .post-card, .metric-card {{
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05), 0 4px 10px -2px rgba(0, 0, 0, 0.02);
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .post-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 20px 40px -5px rgba(0, 119, 181, 0.15);
        border-color: {current_theme['purple_neon']}40;
    }}
    
    /* === INPUTS (Pill/Rounded) === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {{
        background-color: white !important;
        color: {current_theme['deep_black']} !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 0.875rem 1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {current_theme['purple_neon']} !important;
        box-shadow: 0 0 0 4px rgba(0, 119, 181, 0.1) !important;
    }}

    /* === BUTTONS (Gradient & Floating) === */
    button[kind="primary"] {{
        background: linear-gradient(135deg, {current_theme['purple_neon']} 0%, #0091EA 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 10px 20px -5px rgba(0, 119, 181, 0.4) !important;
        transition: all 0.2s !important;
    }}
    
    button[kind="primary"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 15px 25px -5px rgba(0, 119, 181, 0.5) !important;
    }}
    
    div.stButton > button {{
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    
    /* === TABS (Pills) === */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(255,255,255,0.5);
        padding: 0.25rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.8);
        gap: 0;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
        background-color: transparent;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: white !important;
        color: {current_theme['purple_neon']} !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }}

</style>
""", unsafe_allow_html=True)

# Sidebar Branding
with st.sidebar:
    try:
        st.image("assets/logo.png", width=180)
    except:
        st.markdown("### LinPost")
    
    st.markdown("""
    <div style='text-align: center; margin-top: -10px; margin-bottom: 20px;'>
        <p style='font-size: 0.8125rem; color: #374151; font-weight: 500;'>
            Conteúdo inteligente para LinkedIn
        </p>
    </div>
    """, unsafe_allow_html=True)

# Helper for programmatic navigation
def navigate_to(page):
    st.session_state["navigation_selection"] = page
    st.session_state["nav_radio"] = page

# Handle navigation state
if "navigation_selection" not in st.session_state:
    st.session_state["navigation_selection"] = "🏠 Home"

# Sidebar Navigation
# We use index to sync with session state instead of direct key binding to avoid "locked" state issues
current_selection = st.session_state["navigation_selection"]
nav_options = [
    "🏠 Home", 
    "📊 Dashboard",
    "✨ Gerador de Posts", 
    "📚 Biblioteca",
    "📅 Agendamento",
    "🎙️ Criar de Mídia", 
    "📡 News Radar", 
    "⚙️ Configurações"
]

try:
    current_index = nav_options.index(current_selection)
except ValueError:
    current_index = 0

page = st.sidebar.radio(
    "Navegação", 
    nav_options,
    # index=current_index,  <-- REMOVED TO FIX WARNING. Key is sufficient.
    # When key is provided, Streamlit uses session state.
    # If we provide index AND key, and they differ from session state, it warns.
    key="nav_radio",
    on_change=lambda: navigate_to(st.session_state.nav_radio)
)

# Keyboard shortcuts hint
st.sidebar.markdown("---")
st.sidebar.markdown("### ⌨️ Atalhos")
st.sidebar.markdown("""
<small style='color: #6B7280;'>
• <kbd>Ctrl+S</kbd> Salvar post<br>
• <kbd>Ctrl+Enter</kbd> Gerar post<br>
• <kbd>Esc</kbd> Limpar editor
</small>
""", unsafe_allow_html=True)

if page == "🏠 Home":
    # Hero Section - Mobile App Style
    st.markdown(f"""
    <div style='text-align: left; padding: 1rem 0 2rem 0;'>
        <h1 style='font-size: 2.25rem; margin-bottom: 0.5rem;'>
            Bem-vindo ao LinPost
        </h1>
        <p style='font-size: 1.125rem; color: {current_theme['graphite']}; max-width: 600px; line-height: 1.5;'>
            Sua central inteligente para conteúdo, ideias e posts usando IA.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid Layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Generator Card
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">✨</div>
            <h3 style="margin-bottom: 0.5rem; color: {current_theme['deep_black']};">Gerador de Conteúdo</h3>
            <p style="font-size: 0.875rem; color: {current_theme['graphite']};">Crie posts virais com IA em segundos.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Criar Novo Post", use_container_width=True, type="primary", on_click=navigate_to, args=("✨ Gerador de Posts",)):
            pass

        st.markdown("<br>", unsafe_allow_html=True)

        # Analytics/Radar Card (using placeholder for now)
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📡</div>
            <h3 style="margin-bottom: 0.5rem; color: {current_theme['deep_black']};">News Radar</h3>
            <p style="font-size: 0.875rem; color: {current_theme['graphite']};">Tendências e notícias em tempo real.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📡 Ver Notícias", use_container_width=True, on_click=navigate_to, args=("📡 News Radar",)):
            pass

    with col2:
        # Scheduling Card
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📅</div>
            <h3 style="margin-bottom: 0.5rem; color: {current_theme['deep_black']};">Agendamento</h3>
            <p style="font-size: 0.875rem; color: {current_theme['graphite']};">Visualize e gerencie seu calendário.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗓️ Ver Calendário", use_container_width=True, on_click=navigate_to, args=("📅 Agendamento",)):
            pass

        st.markdown("<br>", unsafe_allow_html=True)

        # Media Card
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎙️</div>
            <h3 style="margin-bottom: 0.5rem; color: {current_theme['deep_black']};">Criar Mídia</h3>
            <p style="font-size: 0.875rem; color: {current_theme['graphite']};">Gere imagens e áudios para seus posts.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎨 Criar Visual", use_container_width=True, on_click=navigate_to, args=("🎙️ Criar de Mídia",)):
            pass

    st.markdown("---")
    
    st.markdown("---")

    
elif page == "📊 Dashboard":
    st.markdown("### 📊 Dashboard Geral")
    
    from src import analytics
    # Get metrics
    metrics = analytics.get_metrics(30)
    
    # 1. Top Metrics Row
    st.markdown("#### Visão Geral (30 dias)")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Total de Posts", metrics['total_posts'])
    with m_col2:
        st.metric("Sequência", f"{metrics['streak']} dias")
    with m_col3:
        st.metric("Média Palavras", metrics['avg_words'])
    
    st.markdown("---")
    
    # 2. Activity Chart (Moved from Library)
    st.markdown("#### 📈 Atividade de Postagem")
    dates, counts = analytics.get_posting_activity()
    
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dates,
        y=counts,
        marker_color=current_theme['purple_neon'],
        opacity=0.8
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=350,
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor=current_theme['border_gray']
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=current_theme['soft_gray'],
            showline=False,
            title="Posts"
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. Insights (Moved from Library)
    st.markdown("---")
    st.markdown("#### 💡 Insights Automáticos")
    insights = analytics.get_insights(metrics)
    
    cols_insights = st.columns(len(insights) if insights else 1)
    if insights:
        for idx, insight in enumerate(insights):
            with cols_insights[idx]:
                border_color = current_theme['success'] if insight['type'] == "positive" else current_theme['warning'] if insight['type'] == "tip" else current_theme['cyan_blue']
                st.markdown(f'''
                <div class="post-card" style="border-left: 4px solid {border_color}; padding: 1.25rem; height: 100%;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                        <span style="font-size: 1.25rem; margin-right: 0.5rem;">{insight['icon']}</span>
                        <span style="font-weight: 600; color: {current_theme['deep_black']};">{insight['title']}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: {current_theme['graphite']}; line-height: 1.5;">{insight['description']}</div>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.info("Ainda não temos insights suficientes. Continue postando!")

elif page == "📚 Biblioteca":
    st.markdown("### 📚 Sua Biblioteca de Conteúdo")

    # Search and Filter Section
    st.markdown("### 🔍 Buscar Posts")
    
    user_id = st.session_state.user.id
    
    # Search and filter controls
    col_search, col_tags, col_fav = st.columns([3, 2, 1])
    
    with col_search:
        search_query = st.text_input("🔎 Buscar por conteúdo ou tópico", placeholder="Digite para buscar...", label_visibility="collapsed")
    
    with col_tags:
        all_tags = database.get_all_tags(user_id)
        selected_tags = st.multiselect("🏷️ Filtrar por tags", all_tags, placeholder="Todas as tags")
    
    with col_fav:
        show_favorites = st.checkbox("⭐ Favoritos", value=False)
    
    # Search posts
    if search_query or selected_tags or show_favorites:
        posts = database.search_posts(user_id, query=search_query, tags=selected_tags, favorites_only=show_favorites)
    else:
        posts = database.get_posts(user_id)
    
    st.markdown(f"**{len(posts)} posts encontrados**")
    st.markdown("---")
    
    if posts:
        for idx, post in enumerate(posts):
            topic = post.get('topic', 'Sem tópico')
            content = post.get('content', '')
            created_at = post.get('created_at', '')
            post_id = post.get('id')
            post_tags = post.get('tags', [])
            is_favorite = post.get('is_favorite', False)
            
            # Format date
            try:
                date_obj = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%d/%m/%Y às %H:%M')
            except:
                formatted_date = created_at
            
            # Create card with tags
            tags_html = ""
            if post_tags:
                tags_html = "<div style='margin-top: 0.5rem;'>"
                for tag in post_tags:
                    tags_html += f"<span style='background: {current_theme['purple_neon']}; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-right: 0.25rem; display: inline-block;'>🏷️ {tag}</span>"
                tags_html += "</div>"
            
            fav_icon = "⭐" if is_favorite else "☆"
            
            st.markdown(f'''
            <div class="post-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div class="post-topic">{topic}</div>
                    <div style="font-size: 1.5rem; cursor: pointer;">{fav_icon}</div>
                </div>
                <div class="post-meta">📅 {formatted_date} • {len(content)} caracteres</div>
                <div class="post-content">{content}</div>
                {tags_html}
            </div>
            ''', unsafe_allow_html=True)
            
            # Action Buttons Row
            col_actions = st.columns([1, 1, 1, 3])
            
            with col_actions[0]:
                if st.button("🗑️", key=f"del_{idx}", help="Deletar Post"):
                    database.delete_post(post_id)
                    st.rerun()
            
            with col_actions[1]:
                fav_label = "⭐" if is_favorite else "☆"
                if st.button(fav_label, key=f"fav_{idx}", help="Favoritar"):
                    database.toggle_favorite(post_id, not is_favorite)
                    st.rerun()
            
            with col_actions[2]:
                if st.button("📋", key=f"copy_{idx}", help="Copiar Conteúdo"):
                    st.code(content, language=None)
                    st.toast("Conteúdo copiado para a área de transferência!", icon="📋")

            with col_actions[3]:
                # Tag management in a cleaner way
                with st.popover("🏷️ Gerenciar Tags"):
                    # Ensure post_tags is always a list
                    safe_post_tags = post_tags if post_tags is not None else []
                    
                    current_tags = st.multiselect(
                        "Tags do post",
                        options=all_tags + ["+ Nova tag"],
                        default=safe_post_tags,
                        key=f"tags_{idx}"
                    )
                    
                    if "+ Nova tag" in current_tags:
                        new_tag = st.text_input("Nome da nova tag", key=f"new_tag_{idx}")
                        if new_tag and st.button("Criar Tag", key=f"add_tag_{idx}"):
                            current_tags.remove("+ Nova tag")
                            current_tags.append(new_tag)
                            database.update_post_tags(post_id, current_tags)
                            st.rerun()
                    
                    # Safe comparison
                    if set(current_tags) != set(safe_post_tags) and "+ Nova tag" not in current_tags:
                        if st.button("Salvar Alterações", key=f"save_tags_{idx}"):
                            database.update_post_tags(post_id, current_tags)
                            st.rerun()
    else:
        if search_query or selected_tags or show_favorites:
            st.info("🔍 Nenhum post encontrado com esses filtros.")
        else:
            st.info("🎯 Nenhum post encontrado. Vá ao Gerador de Posts para criar um!")



elif page == "✨ Gerador de Posts":
    from src import ai_helpers, templates, resources
    
    # Hero Section
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h1 style='font-size: 2.25rem; margin-bottom: 0.5rem; color: {current_theme['deep_black']};'>
            ✨ Gerador de Conteúdo com IA
        </h1>
        <p style='font-size: 1rem; color: {current_theme['graphite']};'>
            Transforme qualquer ideia em um post pronto para publicar.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Templates Library
    with st.expander("📚 Biblioteca de Templates", expanded=False):
        st.markdown("**Escolha um template para começar:**")
        template_category = st.selectbox("Categoria", templates.get_categories(), key="template_cat")
        
        category_templates = templates.get_templates(template_category)
        cols = st.columns(2)
        for idx, template in enumerate(category_templates):
            with cols[idx % 2]:
                if st.button(f"📄 {template['title']}", key=f"tmpl_{idx}", use_container_width=True):
                    st.session_state['last_post'] = template['content']
                    st.session_state['last_topic'] = template['title']
                    st.success(f"✅ Template '{template['title']}' carregado!")
                    st.rerun()
    
    # Resources Library
    with st.expander("🎨 Biblioteca de Recursos", expanded=False):
        tab1, tab2, tab3 = st.tabs(["😊 Emojis", "📣 CTAs", "💡 Frases de Impacto"])
        
        with tab1:
            emoji_cat = st.selectbox("Categoria de Emoji", resources.get_emoji_categories())
            emojis = resources.get_emojis(emoji_cat)
            cols = st.columns(8)
            for idx, emoji in enumerate(emojis):
                with cols[idx % 8]:
                    if st.button(emoji, key=f"emoji_{idx}"):
                        if 'last_post' in st.session_state:
                            st.session_state['last_post'] += emoji
                            st.rerun()
        
        with tab2:
            st.markdown("**Clique para adicionar ao post:**")
            ctas = resources.get_ctas()
            for idx, cta in enumerate(ctas[:5]):  # Show first 5
                if st.button(f"➕ {cta}", key=f"cta_{idx}", use_container_width=True):
                    if 'last_post' in st.session_state:
                        st.session_state['last_post'] += f"\n\n{cta}"
                        st.rerun()
        
        with tab3:
            st.markdown("**Frases poderosas para começar:**")
            phrases = resources.get_power_phrases()
            for idx, phrase in enumerate(phrases[:5]):  # Show first 5
                if st.button(f"✨ {phrase}", key=f"phrase_{idx}", use_container_width=True):
                    if 'last_post' in st.session_state:
                        st.session_state['last_post'] = f"{phrase}\n\n{st.session_state.get('last_post', '')}"
                        st.rerun()
    
    # Post Generation Form
    with st.form(key="post_generator_form", clear_on_submit=False):
        st.markdown(f"""
        <div style='margin-bottom: 0.75rem;'>
            <span style='color: {current_theme['deep_black']}; font-size: 0.875rem; font-weight: 600;'>
                💡 Sobre o que você quer escrever?
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            topic = st.text_input(
                "topic",
                value="",
                placeholder="Ex.: Como IA está mudando o marketing, experiência do cliente em 2025, aprendizados da semana...",
                label_visibility="collapsed"
            )
        
        with col2:
            tone = st.selectbox(
                "Tom do post",
                ["Profissional", "Casual inteligente", "Inspirador", "Direto e provocativo", "Storytelling humano"],
                label_visibility="collapsed"
            )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Gerar Post", use_container_width=True, type="primary")
    
    # Process form submission
    if submitted:
        if topic:
            with st.spinner("✨ Gerando seu post..."):
                content = generator.generate_post(topic, tone)
                st.session_state['last_post'] = content
                st.session_state['last_topic'] = topic
                st.success("✅ Post gerado com sucesso!")
        else:
            st.warning("⚠️ Por favor, insira um tópico.")
    
    if 'last_post' in st.session_state:
        st.markdown("---")
        
        # Two columns: Editor and Preview
        col_editor, col_preview = st.columns([1, 1])
        
        with col_editor:
            st.markdown("### ✏️ Editor")
            
            content = st.text_area(
                "Edite o conteúdo:",
                st.session_state['last_post'],
                height=300,
                key="generated_content"
            )
            
            # Stats row
            word_count = ai_helpers.count_words(content)
            sentence_count = ai_helpers.count_sentences(content)
            char_count = len(content)
            readability = ai_helpers.analyze_readability(content)
            
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            with col_stat1:
                st.metric("Palavras", word_count)
            with col_stat2:
                st.metric("Frases", sentence_count)
            with col_stat3:
                linkedin_limit = 3000
                st.metric("Caracteres", f"{char_count}/{linkedin_limit}")
            with col_stat4:
                st.metric("Leitura", readability)
            
            # Hashtag suggestions
            st.markdown("#### 🏷️ Sugestões de Hashtags")
            suggested_tags = ai_helpers.suggest_hashtags(content, st.session_state['last_topic'])
            
            cols = st.columns(3)
            for idx, tag in enumerate(suggested_tags):
                with cols[idx % 3]:
                    # Using custom HTML for better styling, but buttons are limited in Streamlit
                    # We'll stick to buttons but maybe we can inject CSS to make them look like pills?
                    # Actually, let's just use the button but maybe add a class if possible?
                    # Streamlit buttons are hard to style individually.
                    # Let's just keep the button for functionality but maybe change the text?
                    if st.button(f"#{tag}", key=f"tag_{idx}", use_container_width=True):
                        if tag not in content:
                            st.session_state['last_post'] = content + " #" + tag
                            st.rerun()
        
        with col_preview:
            st.markdown("### 📱 Preview Mobile")
            
            # Define user_id for preview
            user_id = st.session_state.user.id
            
            # Content score
            score, feedback = ai_helpers.score_content(content)
            
            # Score display with color
            if score >= 80:
                score_color = "#10b981"
                score_label = "Excelente"
            elif score >= 60:
                score_color = "#f59e0b"
                score_label = "Bom"
            else:
                score_color = "#ef4444"
                score_label = "Precisa melhorar"
            
            st.markdown(f"""
            <div style="
                background: {score_color};
                color: white;
                padding: 1rem;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 1rem;
            ">
                <div style="font-size: 2rem; font-weight: bold;">{score}/100</div>
                <div>{score_label}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Feedback list
            with st.expander("📊 Ver análise detalhada", expanded=False):
                for item in feedback:
                    st.markdown(f"- {item}")
            
            # Mobile LinkedIn preview (iPhone style)
            import html
            escaped_content = html.escape(content)
            
            st.markdown(f"""
            <div class="mobile-preview-container">
                <div class="mobile-notch"></div>
                <div style="padding: 2.5rem 1.25rem 1.5rem 1.25rem; height: 100%; overflow-y: auto; font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
                    <!-- Fake Header -->
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <div style="width: 32px; height: 32px; background: #e5e7eb; border-radius: 50%; margin-right: 0.5rem;"></div>
                        <div>
                            <div style="font-weight: 600; font-size: 0.8rem; color: #374151;">Você</div>
                            <div style="font-size: 0.7rem; color: #6b7280;">Agora • 🌐</div>
                        </div>
                    </div>
                    
                    <!-- Content -->
                    <div style="color: #1f2937; font-size: 0.875rem; line-height: 1.5; white-space: pre-wrap; word-wrap: break-word;">
{escaped_content}
                    </div>
                    
                    <!-- Fake Actions -->
                    <div style="margin-top: 1rem; border-top: 1px solid #f3f4f6; padding-top: 0.75rem; display: flex; justify-content: space-between; color: #6b7280; font-size: 1rem; padding-left: 0.5rem; padding-right: 0.5rem;">
                        <span>👍</span> <span>💬</span> <span>🔁</span> <span>✈️</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


        
        st.markdown("---")
        
        # ============================================
        # ADVANCED AI FEATURES
        # ============================================
        from src import advanced_ai
        
        st.markdown("### 🤖 Análise Avançada com IA")
        
        # Create tabs for different AI features
        tab1, tab2, tab3, tab4 = st.tabs([
            "😊 Sentimento", 
            "🎭 Variações", 
            "💡 Sugestões", 
            "📈 Engajamento"
        ])
        
        # TAB 1: Sentiment Analysis
        with tab1:
            st.markdown("#### Análise de Sentimento")
            
            with st.spinner("Analisando tom emocional..."):
                sentiment_result = advanced_ai.analyze_sentiment(content)
            
            # Display sentiment with colored badge
            sentiment_colors = {
                'positive': '#22C55E',
                'neutral': '#6B7280',
                'negative': '#EF4444'
            }
            sentiment_labels = {
                'positive': 'Positivo',
                'neutral': 'Neutro',
                'negative': 'Negativo'
            }
            sentiment_icons = {
                'positive': '😊',
                'neutral': '😐',
                'negative': '😢'
            }
            
            sentiment = sentiment_result['sentiment']
            color = sentiment_colors.get(sentiment, '#6B7280')
            label = sentiment_labels.get(sentiment, 'Neutro')
            icon = sentiment_icons.get(sentiment, '😐')
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="
                    background: {color}15;
                    border-left: 4px solid {color};
                    padding: 1.5rem;
                    border-radius: 8px;
                ">
                    <div style="font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-size: 1.25rem; font-weight: 600; text-align: center; color: {color};">{label}</div>
                    <div style="font-size: 0.875rem; text-align: center; color: #6B7280; margin-top: 0.25rem;">
                        Score: {sentiment_result['score']}/100
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="
                    background: {current_theme['purple_neon']}15;
                    border-left: 4px solid {current_theme['purple_neon']};
                    padding: 1.5rem;
                    border-radius: 8px;
                ">
                    <div style="font-size: 0.875rem; font-weight: 600; color: {current_theme['deep_black']}; margin-bottom: 0.5rem;">
                        Emoção Detectada
                    </div>
                    <div style="font-size: 1.125rem; font-weight: 600; color: {current_theme['purple_neon']};">
                        {sentiment_result['emotion'].capitalize()}
                    </div>
                    <div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.5rem;">
                        Confiança: {int(sentiment_result['confidence'] * 100)}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # TAB 2: Post Variations
        with tab2:
            st.markdown("#### Gerar Variações do Post")
            st.markdown("Crie versões alternativas com diferentes estilos de escrita.")
            
            if st.button("🎭 Gerar 3 Variações", use_container_width=True, key="generate_variations"):
                with st.spinner("Gerando variações criativas..."):
                    variations = advanced_ai.generate_variations(content, st.session_state['last_topic'], num_variations=3)
                    st.session_state['variations'] = variations
            
            if 'variations' in st.session_state and st.session_state['variations']:
                st.markdown("---")
                for idx, variation in enumerate(st.session_state['variations']):
                    with st.expander(f"📝 {variation['style']}", expanded=(idx == 0)):
                        st.markdown(variation['content'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"✅ Usar esta versão", key=f"use_var_{idx}", use_container_width=True):
                                st.session_state['last_post'] = variation['content']
                                st.rerun()
                        with col2:
                            if st.button(f"📋 Copiar", key=f"copy_var_{idx}", use_container_width=True):
                                st.code(variation['content'], language=None)
                                st.toast("Variação copiada!", icon="📋")
        
        # TAB 3: Real-time Suggestions
        with tab3:
            st.markdown("#### Sugestões de Melhoria")
            
            suggestions = advanced_ai.get_realtime_suggestions(content)
            
            if suggestions:
                for suggestion in suggestions:
                    if suggestion['type'] == 'warning':
                        st.warning(suggestion['message'])
                    elif suggestion['type'] == 'tip':
                        st.info(suggestion['message'])
                    elif suggestion['type'] == 'success':
                        st.success(suggestion['message'])
            else:
                st.success("✅ Seu post está ótimo! Nenhuma sugestão no momento.")
        
        # TAB 4: Engagement Prediction
        with tab4:
            st.markdown("#### Previsão de Engajamento")
            
            engagement = advanced_ai.predict_engagement(content, st.session_state['last_topic'])
            
            # Overall score with color
            score = engagement['score']
            level = engagement['level']
            
            level_colors = {
                'baixo': '#EF4444',
                'médio': '#F59E0B',
                'alto': '#22C55E',
                'viral': '#8B5CF6'
            }
            level_icons = {
                'baixo': '📉',
                'médio': '📊',
                'alto': '📈',
                'viral': '🚀'
            }
            
            level_color = level_colors.get(level, '#6B7280')
            level_icon = level_icons.get(level, '📊')
            
            st.markdown(f"""
            <div style="
                background: {level_color}15;
                border: 2px solid {level_color};
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                margin-bottom: 1rem;
            ">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">{level_icon}</div>
                <div style="font-size: 2rem; font-weight: 700; color: {level_color};">{score}/100</div>
                <div style="font-size: 1rem; font-weight: 600; color: {current_theme['deep_black']}; margin-top: 0.5rem;">
                    Potencial: {level.upper()}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Breakdown of factors
            st.markdown("**Análise Detalhada:**")
            
            factors = engagement['factors']
            for factor_name, factor_score in factors.items():
                factor_labels = {
                    'length': 'Tamanho',
                    'structure': 'Estrutura',
                    'hooks': 'Gancho Inicial',
                    'cta': 'Call-to-Action',
                    'hashtags': 'Hashtags'
                }
                
                label = factor_labels.get(factor_name, factor_name)
                
                # Progress bar color based on score
                if factor_score >= 80:
                    bar_color = '#22C55E'
                elif factor_score >= 60:
                    bar_color = '#F59E0B'
                else:
                    bar_color = '#EF4444'
                
                st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span style="font-size: 0.875rem; font-weight: 600;">{label}</span>
                        <span style="font-size: 0.875rem; color: {bar_color}; font-weight: 600;">{factor_score}/100</span>
                    </div>
                    <div style="background: #E5E7EB; border-radius: 10px; height: 8px; overflow: hidden;">
                        <div style="background: {bar_color}; width: {factor_score}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendations
            if engagement['recommendations']:
                st.markdown("**💡 Recomendações:**")
                for rec in engagement['recommendations']:
                    st.markdown(f"- {rec}")
        
        st.markdown("---")
        
        # Tags selector
        st.markdown("#### 🏷️ Adicionar Tags")
        user_id = st.session_state.user.id
        existing_tags = database.get_all_tags(user_id)
        post_tags = st.multiselect(
            "Selecione ou crie tags para organizar este post:",
            options=existing_tags + ["+ Nova tag"],
            key="post_tags_selector"
        )
        
        # Handle new tag creation
        if "+ Nova tag" in post_tags:
            post_tags.remove("+ Nova tag")
            new_tag = st.text_input("Digite a nova tag:", key="new_post_tag", placeholder="Ex: Vendas, Marketing, Tech...")
            if new_tag:
                post_tags.append(new_tag)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Salvar no Banco de Dados", use_container_width=True):
                result = database.create_post(user_id, content, st.session_state['last_topic'], tags=post_tags)
                if result:
                    st.success("✅ Post salvo com sucesso!")
                    st.success("✅ Post gerado com sucesso!")
                else:
                    st.error("❌ Erro ao salvar.")

        
        with col2:
            from src import linkedin
            if linkedin.is_connected():
                if st.button("🔗 Publicar no LinkedIn", use_container_width=True):
                    success, message = linkedin.post_to_linkedin(content)
                    if success:
                        st.success(message)
                        st.success("✅ Post gerado com sucesso!")
                    else:
                        st.error(message)
            else:
                st.info("Conecte o LinkedIn nas Configurações")
        
        with col3:
            if st.button("📋 Copiar para Clipboard", use_container_width=True):
                st.code(content, language=None)
                st.info("👆 Copie o texto acima!")


elif page == "📅 Agendamento":
    from src import scheduling_ui
    scheduling_ui.render_scheduling_page(current_theme)


elif page == "🎙️ Criar de Mídia":
    # Hero Section
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h1 style='font-size: 2.25rem; margin-bottom: 0.5rem; color: {current_theme['deep_black']};'>
            🎙️ Studio Criativo
        </h1>
        <p style='font-size: 1rem; color: {current_theme['graphite']};'>
            Transforme seus arquivos de mídia em posts virais.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Selection Cards
    col_media1, col_media2 = st.columns(2)
    
    # State management for media type
    if "media_mode" not in st.session_state:
        st.session_state["media_mode"] = "image"
        
    with col_media1:
        # Image Card
        is_active = st.session_state["media_mode"] == "image"
        bg_color = current_theme['light_blue'] if is_active else "white"
        border_color = current_theme['purple_neon'] if is_active else "transparent"
        
        st.markdown(f"""
        <div style="
            background: {bg_color};
            border: 2px solid {border_color};
            border-radius: 16px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📸</div>
            <h3 style="margin: 0; color: {current_theme['deep_black']}; font-size: 1.1rem;">Post de Imagem</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Selecionar Imagem", key="btn_mode_img", use_container_width=True):
            st.session_state["media_mode"] = "image"
            st.rerun()

    with col_media2:
        # Audio Card
        is_active = st.session_state["media_mode"] == "audio"
        bg_color = current_theme['light_blue'] if is_active else "white"
        border_color = current_theme['purple_neon'] if is_active else "transparent"
        
        st.markdown(f"""
        <div style="
            background: {bg_color};
            border: 2px solid {border_color};
            border-radius: 16px;
            padding: 1.5rem;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎙️</div>
            <h3 style="margin: 0; color: {current_theme['deep_black']}; font-size: 1.1rem;">Post de Áudio</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Selecionar Áudio", key="btn_mode_audio", use_container_width=True):
            st.session_state["media_mode"] = "audio"
            st.rerun()
            
    st.markdown("---")

    if st.session_state["media_mode"] == "image":
        st.markdown(f"""
        <div style="background: white; border-radius: 16px; padding: 2rem; border: 2px dashed {current_theme['border_gray']}; text-align: center;">
            <p style="font-weight: 500; margin-bottom: 1rem;">Arraste sua imagem aqui</p>
        </div>
        """, unsafe_allow_html=True)
        
        # We place the uploader "inside" via visual proximity, though Streamlit limitations apply
        uploaded_img = st.file_uploader("Upload de imagem", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if uploaded_img:
            col_preview, col_form = st.columns([1, 2])
            
            with col_preview:
                st.image(uploaded_img, caption="Preview", use_container_width=True)
            
            with col_form:
                st.markdown("### 🪄 Configurar Geração")
                img_topic = st.text_input("Contexto (Opcional)", placeholder="Ex: Evento da empresa, Novo produto...")
                
                if st.button("✨ Gerar Post Mágico", type="primary", use_container_width=True):
                    with st.spinner("👀 Analisando pixels..."):
                        # Simulation of Vision API
                        import time
                        time.sleep(2)
                        
                        generated_content = f"""🚀 Que momento incrível!
                        
Acabei de registrar essa imagem que representa muito para mim: {img_topic if img_topic else 'uma conquista importante'}.

Muitas vezes focamos apenas no resultado final, mas o processo é onde a mágica acontece. Essa foto me lembra que cada passo importa.

💡 O que você tem celebrado ultimamente?

#Conquista #Jornada #LinPost"""
                        
                        st.session_state['last_post'] = generated_content
                        st.session_state['last_topic'] = img_topic or "Imagem"
                        st.success("✅ Post gerado! Redirecionando...")
                        time.sleep(1)
                        st.session_state["navigation_selection"] = "✨ Gerador de Posts"
                        st.rerun()

    elif st.session_state["media_mode"] == "audio":
        st.markdown(f"""
        <div style="background: white; border-radius: 16px; padding: 2rem; border: 2px dashed {current_theme['border_gray']}; text-align: center;">
            <p style="font-weight: 500; margin-bottom: 1rem;">Solte seu áudio aqui (Voice memo, Podcast...)</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_audio = st.file_uploader("Upload de áudio", type=['mp3', 'wav', 'm4a', 'ogg'], label_visibility="collapsed")
        
        if uploaded_audio:
            st.audio(uploaded_audio)
            
            if st.button("📝 Transcrever e Gerar Post", type="primary", use_container_width=True):
                with st.spinner("👂 Ouvindo e transcrevendo..."):
                    import time
                    time.sleep(2)
                    
                    transcription = "Olá pessoal, hoje eu queria falar sobre a importância da consistência. Muita gente começa animada mas para no meio do caminho. O segredo é continuar mesmo quando não está motivado."
                    
                    st.markdown(f"""
                    <div style="background: {current_theme['soft_gray']}; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                        <strong>🎙️ Transcrição:</strong><br>
                        <em>"{transcription}"</em>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.spinner("✨ Transformando em post..."):
                        generated_content = f"""💎 A Chave é a Consistência!

"{transcription}"

Hoje refleti sobre isso. A motivação te faz começar, mas é o hábito que te faz continuar.

#Consistencia #Disciplina #LinPost"""
                        
                        st.session_state['last_post'] = generated_content
                        st.session_state['last_topic'] = "Transcrição de Áudio"
                        
                        st.success("✅ Post gerado! Redirecionando...")
                        time.sleep(1)
                        st.session_state["navigation_selection"] = "✨ Gerador de Posts"
                        st.rerun()


elif page == "📡 News Radar":
    from src import news
    
    # Hero Section
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h1 style='font-size: 2.25rem; margin-bottom: 0.5rem; color: {current_theme['deep_black']};'>
            🛰️ News Radar
        </h1>
        <p style='font-size: 1rem; color: {current_theme['graphite']};'>
            Monitore tendências e crie conteúdo atualizado em segundos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if API key is configured
    api_key = news.get_news_api_key()
    if not api_key:
        st.warning("⚠️ **NewsAPI não configurada**")
        st.info("Para usar o News Radar, adicione `NEWS_API_KEY` nos secrets do Streamlit Cloud.")
        st.markdown("Obtenha sua chave gratuita em: [NewsAPI.org](https://newsapi.org)")
    else:
        # Search Container
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            border: 1px solid {current_theme['border_gray']};
            margin-bottom: 2rem;
        ">
        """, unsafe_allow_html=True)
        
        col_search, col_lang, col_btn = st.columns([3, 1, 1])
        
        with col_search:
            search_topic = st.text_input(
                "🔎 Tópico",
                placeholder="Ex.: Inteligência Artificial, Startups...",
                label_visibility="collapsed",
                key="news_search"
            )
        
        with col_lang:
            language = st.selectbox(
                "Idioma",
                options=[("Português", "pt"), ("Inglês", "en"), ("Espanhol", "es")],
                format_func=lambda x: x[0],
                label_visibility="collapsed",
                key="news_lang"
            )
            
        with col_btn:
            if st.button("Buscar", use_container_width=True, type="primary"):
                if search_topic:
                    with st.spinner("Reading the web..."):
                        articles = news.fetch_news(search_topic, language=language[1])
                        st.session_state['news_articles'] = articles
                        st.session_state['news_topic'] = search_topic
                else:
                    st.warning("Digite um tópico.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display results
        if 'news_articles' in st.session_state and st.session_state['news_articles']:
            articles = st.session_state['news_articles']
            st.markdown(f"### Destaques para '{st.session_state['news_topic']}'")
            
            # Display articles in a nicer grid
            # Using CSS Grid via markdown for better control or just Columns iterating
            
            for article in articles:
                # Article Card
                with st.container():
                    col_img, col_txt = st.columns([1, 3])
                    
                    with col_img:
                        if article.get('urlToImage'):
                            st.image(article['urlToImage'], use_container_width=True)
                        else:
                            st.markdown(f"""
                            <div style="
                                height: 120px;
                                background: linear-gradient(135deg, {current_theme['soft_gray']} 0%, #e0e0e0 100%);
                                border-radius: 12px;
                                display: flex; align-items: center; justify-content: center;
                                font-size: 2rem;
                            ">📰</div>
                            """, unsafe_allow_html=True)
                            
                    with col_txt:
                        st.markdown(f"""
                        <h4 style="margin: 0; color: {current_theme['deep_black']};">{article['title']}</h4>
                        <p style="font-size: 0.8rem; color: #6B7280; margin: 0.2rem 0;">
                            {article['source']['name']} • {article.get('publishedAt', 'N/A')[:10]}
                        </p>
                        <p style="font-size: 0.9rem; color: {current_theme['graphite']}; line-height: 1.4;">
                            {article.get('description', '')[:150]}...
                        </p>
                        """, unsafe_allow_html=True)
                        
                        btn_col1, btn_col2 = st.columns([1, 2])
                        with btn_col1:
                             st.link_button("Ler Mais", article['url'], use_container_width=True)
                        with btn_col2:
                            if st.button(f"✨ Criar Post sobre isso", key=f"btn_art_{article['url']}", use_container_width=True):
                                # Logic to generate post
                                news_context = news.format_news_for_prompt(article)
                                with st.spinner("Gerando conteúdo..."):
                                    from src import generator
                                    prompt = f"Escreva um post para LinkedIn sobre: {news_context}"
                                    content = generator.generate_post(prompt, tone="Profissional")
                                    st.session_state['last_post'] = content
                                    st.session_state['last_topic'] = article['title']
                                    st.session_state["navigation_selection"] = "✨ Gerador de Posts"
                                    st.rerun()
                                    
                    st.markdown("---")
        
        elif 'news_articles' in st.session_state and not st.session_state['news_articles']:
            st.info("🔍 Nenhuma notícia encontrada. Tente outro tópico.")

elif page == "⚙️ Configurações":
    from src import linkedin
    
    # Hero Section
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h1 style='font-size: 2.25rem; margin-bottom: 0.5rem; color: {current_theme['deep_black']};'>
            ⚙️ Configurações
        </h1>
        <p style='font-size: 1rem; color: {current_theme['graphite']};'>
            Gerencie suas integrações e preferências.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # LinkedIn Integration Card
    st.markdown("### 🔗 Integração LinkedIn")
    
    is_connected = linkedin.is_connected()
    status_color = current_theme['success'] if is_connected else current_theme['warning']
    status_icon = "✅" if is_connected else "⚠️"
    status_text = "Conectado" if is_connected else "Desconectado"
    
    user_info = ""
    if is_connected:
        user_data = st.session_state.get('linkedin_user', {})
        user_name = user_data.get('name', 'Usuário')
        user_info = f"<p style='margin: 0.5rem 0 0 0; font-weight: 500;'>👤 {user_name}</p>"
    
    st.markdown(f"""
<div class="post-card" style="border-left: 4px solid {status_color};">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div>
<h3 style="margin: 0; color: {current_theme['deep_black']};">Status da Conexão</h3>
<p style="margin: 0.2rem 0; color: {current_theme['graphite']};">
{status_icon} <strong>{status_text}</strong>
</p>
{user_info}
</div>
<div style="font-size: 2rem;">🔗</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if is_connected:
        if st.button("🔓 Desconectar LinkedIn", use_container_width=True):
            linkedin.disconnect_linkedin()
            st.rerun()
    else:
        auth_url = linkedin.get_authorization_url()
        if auth_url:
            st.link_button("🔗 Conectar Conta do LinkedIn", auth_url, type="primary", use_container_width=True)
        else:
            st.error("⚠️ Credenciais não configuradas. Verifique seus secrets.")
            
    st.markdown("---")
    
    # API Keys Section
    st.markdown("### 🔑 Chaves de API")
    
    st.markdown(f"""
<div class="post-card">
<div style="display: flex; align-items: start;">
<span style="font-size: 1.5rem; margin-right: 1rem;">🛡️</span>
<div>
<h4 style="margin: 0; color: {current_theme['deep_black']};">Gerenciamento de Segredos</h4>
<p style="font-size: 0.9rem; color: {current_theme['graphite']}; margin-top: 0.5rem;">
As chaves de API (OpenAI, LinkedIn, Supabase) são gerenciadas de forma segura através do arquivo <code>secrets.toml</code> do Streamlit.
</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

