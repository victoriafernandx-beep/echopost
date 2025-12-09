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
current_theme = {
    # Primary Colors
    "purple_neon": "#8B5CF6",      # Brand identity, icons, highlights
    "cyan_blue": "#0EA5E9",        # Primary actions, buttons
    "deep_black": "#0D0D0D",       # Main text
    
    # Secondary Colors
    "soft_gray": "#F3F4F6",        # Card backgrounds
    "graphite": "#374151",         # Secondary text
    "border_gray": "#E5E7EB",      # Borders, dividers
    "light_lilac": "#C4B5FD",      # Subtle details
    "light_blue": "#7DD3FC",       # Hover states
    
    # Feedback Colors
    "success": "#22C55E",
    "warning": "#FACC15",
    "error": "#EF4444",
    
    # Backgrounds
    "bg_main": "#FFFFFF",
    "bg_sidebar": "#FFFFFF",
    "card_bg": "#F9FAFB"
}

st.markdown(f"""
<style>
    /* LinPost Premium Design System */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    /* === TYPOGRAPHY === */
    .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: {current_theme['bg_main']};
    }}
    
    h1, h2, h3 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
    
    h1 {{
        color: {current_theme['deep_black']} !important;
        font-size: 2.125rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 0.5rem !important;
    }}
    
    h2 {{
        color: {current_theme['deep_black']} !important;
        font-size: 1.625rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 0.75rem !important;
    }}
    
    h3 {{
        color: {current_theme['deep_black']} !important;
        transform: translateY(-1px) !important;
    }}
    
    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {{
        background: {current_theme['bg_sidebar']};
        border-right: 1px solid {current_theme['border_gray']};
        padding-top: 1.5rem;
    }}
    
    /* Hide the radio button circle/icon using aggressive selectors */
    section[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-of-type,
    section[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-of-type {{
        display: none !important;
    }}
    
    /* Container spacing */
    section[data-testid="stSidebar"] [role="radiogroup"] {{
        gap: 0.5rem;
    }}

    /* Style the label container */
    section[data-testid="stSidebar"] [data-baseweb="radio"],
    section[data-testid="stSidebar"] [role="radiogroup"] > label {{
        background: transparent !important;
        color: {current_theme['graphite']} !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        cursor: pointer !important;
        border-radius: 8px !important;
        border-left: 3px solid transparent !important;
    }}
    
    /* Hover state */
    section[data-testid="stSidebar"] [data-baseweb="radio"]:hover,
    section[data-testid="stSidebar"] [role="radiogroup"] > label:hover {{
        background: {current_theme['soft_gray']} !important;
        color: {current_theme['purple_neon']} !important;
    }}

    /* Selected state - using aria-checked which Streamlit typically updates */
    section[data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"],
    section[data-testid="stSidebar"] [role="radiogroup"] > label[data-checked="true"] {{
        background: linear-gradient(135deg, {current_theme['purple_neon']}15 0%, {current_theme['cyan_blue']}15 100%) !important;
        color: {current_theme['purple_neon']} !important;
        font-weight: 600 !important;
        border-left: 3px solid {current_theme['purple_neon']} !important;
    }}

    /* Ensure text color inherits correctly */
    section[data-testid="stSidebar"] [data-baseweb="radio"] div,
    section[data-testid="stSidebar"] [role="radiogroup"] label div {{
        color: inherit !important;
    }}
    
    /* === INPUTS === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {{
        background-color: white !important;
        color: {current_theme['deep_black']} !important;
        border-radius: 8px !important;
        border: 1.5px solid {current_theme['border_gray']} !important;
        font-size: 0.9375rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {current_theme['purple_neon']} !important;
        box-shadow: 0 0 0 3px {current_theme['purple_neon']}20 !important;
    }}
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: #9CA3AF !important;
        opacity: 1 !important;
    }}
    
    .stTextInput label, .stTextArea label, .stSelectbox label {{
    }}
    
    /* === MOBILE PREVIEW === */
    .mobile-preview-container {{
        border: 10px solid {current_theme['deep_black']};
        border-radius: 28px;
        overflow: hidden;
        max-width: 300px;
        margin: 0 auto;
        background: white;
        position: relative;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }}
    
    .mobile-notch {{
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 90px;
        height: 18px;
        background: {current_theme['deep_black']};
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
        z-index: 10;
    }}
    
    /* === EXPANDER === */
    .streamlit-expanderHeader {{
        background: {current_theme['soft_gray']} !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    
    /* === SUCCESS/ERROR MESSAGES === */
    .stSuccess {{
        background: {current_theme['success']}15 !important;
        border-left: 4px solid {current_theme['success']} !important;
        border-radius: 8px !important;
    }}
    
    .stError {{
        background: {current_theme['error']}15 !important;
        border-left: 4px solid {current_theme['error']} !important;
        border-radius: 8px !important;
    }}
    
    .stWarning {{
        background: {current_theme['warning']}15 !important;
        border-left: 4px solid {current_theme['warning']} !important;
        border-radius: 8px !important;
    }}
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        color: {current_theme['graphite']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {current_theme['purple_neon']}15 !important;
        color: {current_theme['purple_neon']} !important;
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

page = st.sidebar.radio("Navegação", [
    "🏠 Home", 
    "✨ Gerador de Posts", 
    "📅 Agendamento",
    "🎙️ Criar de Mídia", 
    "📡 News Radar", 
    "⚙️ Configurações"
])

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
    from src import analytics
    import plotly.graph_objects as go
    
    # Hero Section
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0 1.5rem 0;'>
        <h1 style='font-size: 2.5rem; margin-bottom: 0.75rem; background: linear-gradient(135deg, {current_theme['purple_neon']} 0%, {current_theme['cyan_blue']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>
            ✨ Bem-vindo ao LinPost
        </h1>
        <p style='font-size: 1.125rem; color: {current_theme['graphite']}; max-width: 600px; margin: 0 auto;'>
            Sua central inteligente para criar conteúdo, ideias e posts usando IA — com consistência e velocidade.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Period selector
    col_title, col_period = st.columns([3, 1])
    with col_title:
        st.markdown("### 📊 Seu painel de criação")
    with col_period:
        period_options = {
            "7 dias": 7,
            "30 dias": 30,
            "90 dias": 90,
            "1 ano": 365
        }
        selected_period = st.selectbox("📅 Período", list(period_options.keys()), index=1, label_visibility="collapsed")
        period_days = period_options[selected_period]
    
    # Get metrics for selected period
    metrics = analytics.get_metrics(period_days)
    
    
    # Metrics Cards with comparison
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="post-card metric-card">
            <div style="color: {current_theme['purple_neon']}; font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
            <div style="font-size: 2rem; font-weight: 700; color: {current_theme['deep_black']}; font-family: 'Plus Jakarta Sans', sans-serif;">{metrics['total_posts']}</div>
            <div style="color: {current_theme['graphite']}; font-size: 0.8125rem; margin-top: 0.25rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Total de Posts</div>
            <div style="color: {current_theme['graphite']}; font-size: 0.75rem; margin-top: 0.25rem;">Quantos posts você já criou aqui</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="post-card metric-card">
            <div style="color: {current_theme['cyan_blue']}; font-size: 2rem; margin-bottom: 0.5rem;">🔥</div>
            <div style="font-size: 2rem; font-weight: 700; color: {current_theme['deep_black']}; font-family: 'Plus Jakarta Sans', sans-serif;">{metrics['posts_in_period']}</div>
            <div style="color: {current_theme['graphite']}; font-size: 0.8125rem; margin-top: 0.25rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Sequência</div>
            <div style="color: {current_theme['success'] if metrics['posts_change'] >= 0 else current_theme['error']}; font-size: 0.75rem; margin-top: 0.25rem; font-weight: 600;">{'+' if metrics['posts_change'] >= 0 else ''}{metrics['posts_change']} <span style="font-weight: 400; color: {current_theme['graphite']};">vs anterior</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="post-card metric-card">
            <div style="color: {current_theme['purple_neon']}; font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <div style="font-size: 2rem; font-weight: 700; color: {current_theme['deep_black']}; font-family: 'Plus Jakarta Sans', sans-serif;">{metrics['avg_words']}</div>
            <div style="color: {current_theme['graphite']}; font-size: 0.8125rem; margin-top: 0.25rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Média de Palavras</div>
            <div style="color: {current_theme['graphite']}; font-size: 0.75rem; margin-top: 0.25rem;">Ideal entre 80-200</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="post-card metric-card">
            <div style="color: {current_theme['cyan_blue']}; font-size: 2rem; margin-bottom: 0.5rem;">🔥</div>
            <div style="font-size: 2rem; font-weight: 700; color: {current_theme['deep_black']}; font-family: 'Plus Jakarta Sans', sans-serif;">{metrics['streak']}</div>
            <div style="color: {current_theme['graphite']}; font-size: 0.8125rem; margin-top: 0.25rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Sequência Ativa</div>
            <div style="color: {current_theme['graphite']}; font-size: 0.75rem; margin-top: 0.25rem;">Dias consecutivos criando</div>
        </div>
        """, unsafe_allow_html=True)
    
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Insights Section
    st.markdown("### 💡 Insights Automáticos")
    insights = analytics.get_insights(metrics)
    
    cols_insights = st.columns(len(insights))
    for idx, insight in enumerate(insights):
        with cols_insights[idx]:
            # Professional styling: White card with colored left border
            border_color = current_theme['success'] if insight['type'] == "positive" else current_theme['warning'] if insight['type'] == "tip" else current_theme['cyan_blue']
            
            st.markdown(f"""
            <div class="post-card" style="border-left: 4px solid {border_color}; padding: 1.25rem; height: 100%;">
                <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                    <span style="font-size: 1.25rem; margin-right: 0.5rem;">{insight['icon']}</span>
                    <span style="font-weight: 600; color: {current_theme['deep_black']};">{insight['title']}</span>
                </div>
                <div style="font-size: 0.9rem; color: {current_theme['graphite']}; line-height: 1.5;">{insight['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two columns: Top Topics and Activity Chart
    col_left, col_right = st.columns([2, 3])
    
    with col_left:
        st.markdown("### 🏷️ Tópicos Mais Usados")
        
        top_topics = analytics.get_top_topics()
        
        if top_topics:
            # Convert to DataFrame for better display
            import pandas as pd
            df = pd.DataFrame(top_topics, columns=['Tópico', 'Posts'])
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Tópico": st.column_config.TextColumn("Tópico"),
                    "Posts": st.column_config.ProgressColumn("Frequência", format="%d", min_value=0, max_value=max([t[1] for t in top_topics]))
                }
            )
        else:
            st.info("Crie posts para ver seus tópicos mais usados!")

    
    with col_right:
        st.markdown("### 📈 Atividade de Postagem (30 dias)")
        
        dates, counts = analytics.get_posting_activity()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=counts,
            marker_color='#2563eb',
            opacity=0.8
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,0.95)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=300,
            xaxis=dict(
                showgrid=False,
                showline=True,
                linecolor='#e5e7eb'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#f3f4f6',
                showline=False,
                title="Posts"
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
                    tags_html += f"<span style='background: #667eea; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-right: 0.25rem; display: inline-block;'>🏷️ {tag}</span>"
                tags_html += "</div>"
            
            fav_icon = "⭐" if is_favorite else "☆"
            
            st.markdown(f"""
            <div class="post-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div class="post-topic">{topic}</div>
                    <div style="font-size: 1.5rem; cursor: pointer;">{fav_icon}</div>
                </div>
                <div class="post-meta">📅 {formatted_date} • {len(content)} caracteres</div>
                <div class="post-content">{content}</div>
                {tags_html}
            </div>
            """, unsafe_allow_html=True)
            
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
    st.markdown("## 🎙️ Criar de Mídia")
    st.markdown("### Transforme imagens e áudios em posts incríveis")
    
    tab_img, tab_audio = st.tabs(["📸 Imagem", "🎤 Áudio"])
    
    with tab_img:
        st.markdown("#### Gerar post a partir de Imagem")
        uploaded_img = st.file_uploader("Faça upload de uma imagem", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_img:
            st.image(uploaded_img, caption="Imagem carregada", width=300)
            img_topic = st.text_input("Sobre o que é essa imagem? (Opcional)", placeholder="Ex: Evento da empresa, Novo produto...")
            
            if st.button("✨ Gerar Post da Imagem", type="primary"):
                with st.spinner("👀 Analisando imagem e gerando post..."):
                    # Placeholder for vision API
                    # In a real app, we'd use GPT-4 Vision or Gemini Vision
                    # For now, we'll simulate or use a text prompt if we can't do vision
                    st.info("🚧 A análise de imagem requer uma API de Visão (GPT-4V ou Gemini Pro Vision).")
                    st.markdown("Simulando geração...")
                    
                    import time
                    time.sleep(2)
                    
                    generated_content = f"""🚀 Que momento incrível!
                    
Acabei de registrar essa imagem que representa muito para mim: {img_topic if img_topic else 'uma conquista importante'}.

Muitas vezes focamos apenas no resultado final, mas o processo é onde a mágica acontece. Essa foto me lembra que cada passo importa.

💡 O que você tem celebrado ultimamente?

#Conquista #Jornada #LinPost"""
                    
                    st.session_state['last_post'] = generated_content
                    st.session_state['last_topic'] = img_topic or "Imagem"
                    st.success("✅ Post gerado! Vá para 'Gerador de Posts' para editar.")
    
    with tab_audio:
        st.markdown("#### Transcrever Áudio e Gerar Post")
        uploaded_audio = st.file_uploader("Faça upload de um áudio", type=['mp3', 'wav', 'm4a', 'ogg'])
        
        if uploaded_audio:
            st.audio(uploaded_audio)
            
            if st.button("📝 Transcrever e Gerar Post", type="primary"):
                with st.spinner("👂 Ouvindo e transcrevendo..."):
                    # Placeholder for Whisper
                    # In real app: transcribe_audio(uploaded_audio)
                    st.info("🚧 A transcrição requer a API Whisper configurada.")
                    st.markdown("Simulando transcrição...")
                    
                    import time
                    time.sleep(2)
                    
                    transcription = "Olá pessoal, hoje eu queria falar sobre a importância da consistência. Muita gente começa animada mas para no meio do caminho. O segredo é continuar mesmo quando não está motivado."
                    
                    st.markdown(f"**Transcrição:** _{transcription}_")
                    st.markdown("---")
                    
                    with st.spinner("✨ Transformando em post..."):
                        generated_content = f"""💎 A Chave é a Consistência!

"{transcription}"

Hoje refleti sobre isso. A motivação te faz começar, mas é o hábito que te faz continuar. Não espere ter vontade para fazer o que precisa ser feito.

Você tem sido consistente nos seus projetos? 👇

#Consistencia #Disciplina #LinPost"""
                        
                        st.session_state['last_post'] = generated_content
                        st.session_state['last_topic'] = "Transcrição de Áudio"
                        st.success("✅ Post gerado! Vá para 'Gerador de Posts' para editar.")


elif page == "📡 News Radar":
    from src import news
    
    # Hero Section
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h1 style='font-size: 2.25rem; margin-bottom: 0.5rem; color: {current_theme['deep_black']};'>
            🛰️ News Radar
        </h1>
        <p style='font-size: 1rem; color: {current_theme['graphite']};'>
            Descubra notícias relevantes e transforme em conteúdo com IA.
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
        # Search interface
        col_search, col_lang = st.columns([3, 1])
        
        with col_search:
            search_topic = st.text_input(
                "🔍 Buscar notícias sobre:",
                placeholder="Ex.: Inteligência Artificial, Tendências de marketing, Startups, Tecnologia...",
                key="news_search"
            )
        
        with col_lang:
            language = st.selectbox(
                "Idioma",
                options=[("Português", "pt"), ("Inglês", "en"), ("Espanhol", "es")],
                format_func=lambda x: x[0],
                key="news_lang"
            )
        
        if st.button("🔎 Buscar Notícias", use_container_width=True, type="primary"):
            if search_topic:
                with st.spinner("🔍 Buscando notícias..."):
                    articles = news.fetch_news(search_topic, language=language[1])
                    st.session_state['news_articles'] = articles
                    st.session_state['news_topic'] = search_topic
            else:
                st.warning("Digite um tópico para buscar.")
        
        # Display results
        if 'news_articles' in st.session_state and st.session_state['news_articles']:
            articles = st.session_state['news_articles']
            st.markdown(f"### 📰 {len(articles)} notícias encontradas sobre '{st.session_state['news_topic']}'")
            st.markdown("---")
            
            # Display articles in grid
            for idx, article in enumerate(articles):
                # Create card
                col_img, col_content = st.columns([1, 2])
                
                with col_img:
                    if article.get('urlToImage'):
                        st.image(article['urlToImage'], use_container_width=True)
                    else:
                        st.markdown("""
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            height: 150px;
                            border-radius: 8px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: white;
                            font-size: 3rem;
                        ">📰</div>
                        """, unsafe_allow_html=True)
                
                with col_content:
                    st.markdown(f"### {article['title']}")
                    st.caption(f"📅 {article.get('publishedAt', 'N/A')[:10]} • 📰 {article['source']['name']}")
                    
                    description = article.get('description', 'Sem descrição disponível.')
                    if len(description) > 200:
                        description = description[:200] + "..."
                    st.markdown(description)
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        st.link_button("🔗 Ler Notícia", article['url'], use_container_width=True)
                    
                    with col_btn2:
                        if st.button("✨ Gerar Post com IA", key=f"gen_news_{idx}", use_container_width=True):
                            # Format news for AI
                            news_context = news.format_news_for_prompt(article)
                            
                            # Generate post
                            with st.spinner("✨ Gerando post..."):
                                from src import generator
                                prompt = f"""Crie um post profissional e envolvente para LinkedIn baseado nesta notícia:
                                
{news_context}

O post deve:
- Começar com um gancho forte
- Apresentar a notícia de forma clara
- Adicionar sua análise ou opinião
- Terminar com uma pergunta para engajamento
- Usar emojis estrategicamente
- Ter entre 150-250 palavras
"""
                                content = generator.generate_post(prompt, tone="Profissional")
                                st.session_state['last_post'] = content
                                st.session_state['last_topic'] = article['title']
                                st.success("✅ Post gerado! Vá para 'Gerador de Posts' para editar e publicar.")
                                st.success("✅ Post gerado com sucesso!")
                
                st.markdown("---")
        
        elif 'news_articles' in st.session_state and not st.session_state['news_articles']:
            st.info("🔍 Nenhuma notícia encontrada. Tente outro tópico ou idioma.")

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
    
    st.markdown("### 🔗 Integração LinkedIn")
    
    if linkedin.is_connected():
        user = st.session_state.get('linkedin_user', {})
        st.success(f"✅ Conectado como: **{user.get('name', 'Usuário')}**")
        
        if st.button("🔓 Desconectar LinkedIn"):
            linkedin.disconnect_linkedin()
            st.rerun()
    else:
        st.info("📌 Conecte sua conta do LinkedIn para publicar posts diretamente do LinPost.")
        
        auth_url = linkedin.get_authorization_url()
        if auth_url:
            st.link_button("🔗 Conectar LinkedIn", auth_url, type="primary", use_container_width=True)
        else:
            st.error("⚠️ Credenciais não configuradas. Verifique os secrets.")
    
    st.markdown("---")
    st.markdown("### 🔑 Chaves de API")
    st.info("Configure suas chaves nos secrets do Streamlit Cloud para habilitar recursos avançados.")

