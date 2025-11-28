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
    page_title="LinPost",
    page_icon="assets/logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme Toggle
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = True

with st.sidebar:
    col_theme, col_void = st.columns([2, 1])
    with col_theme:
        mode_label = "🌙 Modo Escuro" if st.session_state['dark_mode'] else "☀️ Modo Claro"
        if st.button(mode_label, use_container_width=True):
            st.session_state['dark_mode'] = not st.session_state['dark_mode']
            st.rerun()

# Dynamic CSS based on theme
theme_colors = {
    "dark": {
        "bg_main": "#0a0e1a",
        "bg_sidebar": "#111827",
        "card_bg": "#1f2937",
        "text_main": "#f9fafb",
        "text_sec": "#9ca3af",
        "border": "#374151",
        "input_bg": "#111827",
        "metric_val": "#f9fafb"
    },
    "light": {
        "bg_main": "#ffffff",
        "bg_sidebar": "#f8f9fa",
        "card_bg": "#ffffff",
        "text_main": "#1a1a1a",
        "text_sec": "#6b7280",
        "border": "#e5e7eb",
        "input_bg": "#ffffff",
        "metric_val": "#1a1a1a"
    }
}

current_theme = theme_colors["dark"] if st.session_state['dark_mode'] else theme_colors["light"]

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    
    /* Main Background */
    .stApp {{
        background-color: {current_theme['bg_main']};
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {current_theme['bg_sidebar']};
        border-right: 1px solid {current_theme['border']};
    }}
    
    /* Typography */
    h1 {{
        color: {current_theme['text_main']} !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }}
    
    h2 {{
        color: {current_theme['text_main']} !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em !important;
    }}
    
    h3 {{
        color: {current_theme['text_main']} !important;
        font-size: 1.125rem !important;
        font-weight: 600 !important;
    }}
    
    p, label, .stMarkdown, div[data-testid="stMarkdownContainer"] > p {{
        color: {current_theme['text_sec']} !important;
        font-size: 0.875rem !important;
    }}

    /* Cards */
    .post-card {{
        background: {current_theme['card_bg']};
        border: 1px solid {current_theme['border']};
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }}
    
    .metric-card {{
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }}
    
    .post-card:hover {{
        border-color: #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }}
    
    .post-topic {{
        color: #2563eb;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }}
    
    /* Buttons */
    .stButton>button {{
        background: #2563eb;
        color: white !important;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem !important;
        transition: all 0.2s;
    }}
    
    .stButton>button:hover {{
        background: #1d4ed8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }}
    
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{
        background-color: {current_theme['input_bg']} !important;
        color: {current_theme['text_main']} !important;
        border-radius: 6px !important;
        border: 1px solid {current_theme['border']} !important;
        font-size: 0.875rem !important;
        padding: 0.5rem 0.75rem !important;
    }}
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {{
        color: #9ca3af !important;
        opacity: 1 !important;
    }}
    
    .stTextInput label, .stTextArea label, .stSelectbox label {{
        color: {current_theme['text_sec']} !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }}
    
    /* Fix for overlapping labels */
    .stTextInput>div>div, .stTextArea>div>div {{
        position: relative !important;
    }}
    
    .stTextInput label p, .stTextArea label p {{
        margin-bottom: 0.25rem !important;
    }}
    
    /* Hide widget keys that appear in inputs */
    [data-testid="stText"] {{
        display: none !important;
    }}
    
    /* Fix for key text appearing in inputs - more specific */
    .stTextInput div[data-baseweb="input"] > div:first-child {{
        display: none !important;
    }}
    
    .stTextArea div[data-baseweb="textarea"] > div:first-child {{
        display: none !important;
    }}
    
    /* Ensure input text is visible and not overlapped */
    input[type="text"], textarea {{
        position: relative !important;
        z-index: 1 !important;
    }}
    
    /* Aggressive hiding of any text that looks like a key */
    div[class*="st-key"] {{
        display: none !important;
    }}
    
    /* Hide any div containing "key" text pattern */
    .stTextInput > div > div > div:not([data-baseweb]) {{
        display: none !important;
    }}
    
    /* Force hide elements with key-like content */
    .stTextInput [class*="StyledWidgetLabel"] ~ div > div:first-child {{
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }}
    
    /* Metrics Values */
    div[data-testid="stMetricValue"] {{
        color: {current_theme['metric_val']} !important;
        font-size: 1.875rem !important;
        font-weight: 700 !important;
    }}
    
    div[data-testid="stMetricLabel"] {{
        font-size: 0.75rem !important;
        color: {current_theme['text_sec']} !important;
        font-weight: 500 !important;
    }}
    
    /* Hashtags */
    .hashtag-pill {{
        background: rgba(37, 99, 235, 0.05);
        color: #2563eb;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin-right: 4px;
        display: inline-block;
        border: 1px solid rgba(37, 99, 235, 0.1);
    }}

    /* Mobile Preview */
    .mobile-preview-container {{
        border: 10px solid #1e293b;
        border-radius: 28px;
        overflow: hidden;
        max-width: 300px;
        margin: 0 auto;
        background: white;
        position: relative;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }}
    
    .mobile-notch {{
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 90px;
        height: 18px;
        background: #1e293b;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
        z-index: 10;
    }}

</style>
""", unsafe_allow_html=True)

# Sidebar Branding
with st.sidebar:
    try:
        st.image("assets/logo.jpg", width=150)
    except:
        st.title("LinPost")
    
    st.markdown("### Sua plataforma de conteúdo")

page = st.sidebar.radio("Navegação", ["🏠 Home", "✨ Gerador de Posts", "🎙️ Criar de Mídia", "📡 News Radar", "⚙️ Configurações"])

# Keyboard shortcuts hint
st.sidebar.markdown("---")
st.sidebar.markdown("### ⌨️ Atalhos")
st.sidebar.markdown("""
<small>
• Ctrl+S: Salvar post<br>
• Ctrl+Enter: Gerar post<br>
• Esc: Limpar editor
</small>
""", unsafe_allow_html=True)


if page == "🏠 Home":
    from src import analytics
    import plotly.graph_objects as go
    
    st.markdown("## 👋 Bem-vindo ao LinPost")
    
    # Period selector
    col_title, col_period = st.columns([3, 1])
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
            <div style="color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">📝 Total de Posts</div>
            <div style="font-size: 1.875rem; font-weight: 700; color: {current_theme['text_main']};">{metrics['total_posts']}</div>
            <div style="color: {current_theme['text_sec']}; font-size: 0.75rem; margin-top: 0.25rem;">posts criados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="post-card metric-card">
            <div style="color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">📅 Período</div>
            <div style="font-size: 1.875rem; font-weight: 700; color: {current_theme['text_main']};">{metrics['posts_in_period']}</div>
            <div style="color: #10b981; font-size: 0.75rem; margin-top: 0.25rem; font-weight: 600;">{'+' if metrics['posts_change'] >= 0 else ''}{metrics['posts_change']} <span style="font-weight: 400; color: {current_theme['text_sec']};">vs anterior</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="post-card metric-card">
            <div style="color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">🔥 Sequência</div>
            <div style="font-size: 1.875rem; font-weight: 700; color: {current_theme['text_main']};">{metrics['streak']}</div>
            <div style="color: {current_theme['text_sec']}; font-size: 0.75rem; margin-top: 0.25rem;">dias consecutivos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="post-card metric-card">
            <div style="color: #6b7280; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">📏 Média</div>
            <div style="font-size: 1.875rem; font-weight: 700; color: {current_theme['text_main']};">{metrics['avg_words']}</div>
            <div style="color: {current_theme['text_sec']}; font-size: 0.75rem; margin-top: 0.25rem;">palavras/post</div>
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
            border_color = "#10b981" if insight['type'] == "positive" else "#f59e0b" if insight['type'] == "tip" else "#3b82f6"
            
            st.markdown(f"""
            <div class="post-card" style="border-left: 4px solid {border_color}; padding: 1.25rem; height: 100%;">
                <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                    <span style="font-size: 1.25rem; margin-right: 0.5rem;">{insight['icon']}</span>
                    <span style="font-weight: 600; color: {current_theme['text_main']};">{insight['title']}</span>
                </div>
                <div style="font-size: 0.9rem; color: {current_theme['text_sec']}; line-height: 1.5;">{insight['description']}</div>
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
    
    user_id = "test_user"
    
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
    
    st.markdown("## ✨ Gerador de Conteúdo")
    
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
    
    # Input section - using containers to isolate
    input_container = st.container()
    
    with input_container:
        # Custom label outside of input
        st.markdown(f"""
        <div style='margin-bottom: 0.75rem;'>
            <label style='color: {current_theme['text_sec']}; font-size: 0.875rem; font-weight: 500; display: block; margin-bottom: 0.5rem;'>
                💡 Sobre o que você quer escrever?
            </label>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            topic = st.text_input(
                "input_topic_hidden",
                value="",
                placeholder="Ex: Inteligência Artificial no mercado de trabalho",
                key="topic_gen_v2",
                label_visibility="hidden"
            )
        
        with col2:
            st.markdown(f"""
            <div style='margin-bottom: 0.75rem;'>
                <label style='color: {current_theme['text_sec']}; font-size: 0.875rem; font-weight: 500; display: block; margin-bottom: 0.5rem;'>
                    🎭 Tom do post
                </label>
            </div>
            """, unsafe_allow_html=True)
            
            tone = st.selectbox(
                "select_tone_hidden",
                ["Profissional", "Casual", "Inspiracional"],
                key="tone_gen_v2",
                label_visibility="hidden"
            )
    
    if st.button("🚀 Gerar Post", use_container_width=True):
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
            st.markdown(f"""
            <div class="mobile-preview-container">
                <div class="mobile-notch"></div>
                <div style="background: white; min-height: 500px; padding-top: 20px;">
                    <!-- Header -->
                    <div style="padding: 12px; border-bottom: 1px solid #f3f4f6; display: flex; align-items: center; justify-content: space-between;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <div style="width: 32px; height: 32px; border-radius: 50%; background: #e5e7eb; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #666;">
                                👤
                            </div>
                            <div style="background: #eef3f8; padding: 4px 8px; border-radius: 4px; display: flex; align-items: center; gap: 4px;">
                                <span style="color: #0a66c2; font-size: 14px;">🔍</span>
                                <span style="color: #666; font-size: 12px;">Pesquisar</span>
                            </div>
                        </div>
                        <div style="color: #666;">💬</div>
                    </div>
                    
                    <!-- Post -->
                    <div style="padding: 12px;">
                        <!-- User Info -->
                        <div style="display: flex; align-items: flex-start; margin-bottom: 12px;">
                            <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px; margin-right: 10px; flex-shrink: 0;">
                                {user_id[0].upper() if user_id else 'U'}
                            </div>
                            <div style="flex: 1;">
                                <div style="font-weight: 600; color: #1a1a1a; font-size: 14px; line-height: 1.2;">
                                    {st.session_state.get('linkedin_user', {}).get('name', 'Seu Nome')}
                                </div>
                                <div style="font-size: 12px; color: #666; line-height: 1.2; margin-top: 2px;">
                                    {st.session_state.get('linkedin_user', {}).get('headline', 'Criador de Conteúdo | LinPost User')}
                                </div>
                                <div style="font-size: 11px; color: #666; margin-top: 2px;">
                                    1 h • 🌐
                                </div>
                            </div>
                            <div style="color: #666; font-weight: bold;">...</div>
                        </div>
                        
                        <!-- Content -->
                        <div style="color: #1a1a1a; line-height: 1.5; white-space: pre-wrap; word-wrap: break-word; font-size: 14px; margin-bottom: 12px;">
                            {content}
                        </div>
                        
                        <!-- Hashtags (Visual only, if not in content) -->
                        <!-- 
                        <div style="margin-bottom: 12px;">
                            <span style="color: #2563eb; font-weight: 600; font-size: 14px;">#LinPost #Innovation</span>
                        </div>
                        -->
                        
                        <!-- Engagement Stats -->
                        <div style="display: flex; align-items: center; justify-content: space-between; border-top: 1px solid #f3f4f6; padding-top: 8px; margin-bottom: 8px;">
                            <div style="display: flex; align-items: center; gap: 4px;">
                                <span style="font-size: 12px;">👍 👏 ❤️</span>
                                <span style="font-size: 12px; color: #666;">84</span>
                            </div>
                            <div style="font-size: 12px; color: #666;">
                                12 comentários • 4 compartilhamentos
                            </div>
                        </div>
                        
                        <!-- Action Buttons -->
                        <div style="display: flex; justify-content: space-between; border-top: 1px solid #f3f4f6; padding-top: 12px;">
                            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; color: #666;">
                                <span style="font-size: 16px;">👍</span>
                                <span style="font-size: 12px; font-weight: 600;">Gostei</span>
                            </div>
                            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; color: #666;">
                                <span style="font-size: 16px;">💬</span>
                                <span style="font-size: 12px; font-weight: 600;">Comentar</span>
                            </div>
                            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; color: #666;">
                                <span style="font-size: 16px;">🔄</span>
                                <span style="font-size: 12px; font-weight: 600;">Repostar</span>
                            </div>
                            <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; color: #666;">
                                <span style="font-size: 16px;">📤</span>
                                <span style="font-size: 12px; font-weight: 600;">Enviar</span>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Home Indicator -->
                <div style="position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); width: 120px; height: 4px; background: #1a1a1a; border-radius: 2px;"></div>
            </div>
            """, unsafe_allow_html=True)


        
        st.markdown("---")
        
        # Tags selector
        st.markdown("#### 🏷️ Adicionar Tags")
        user_id = "test_user"
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
    
    st.markdown("## 📡 News Radar")
    st.markdown("### Descubra notícias relevantes e gere posts automaticamente")
    
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
                placeholder="Ex: Inteligência Artificial, Tecnologia, Startups...",
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
    
    st.markdown("## ⚙️ Configurações")
    
    st.markdown("### 🔗 Integração LinkedIn")
    
    if linkedin.is_connected():
        user = st.session_state.get('linkedin_user', {})
        st.success(f"✅ Conectado como: **{user.get('name', 'Usuário')}**")
        
        if st.button("🔓 Desconectar LinkedIn"):
            linkedin.disconnect_linkedin()
            st.rerun()
    else:
        st.info("📌 Conecte sua conta do LinkedIn para publicar posts diretamente da plataforma.")
        
        auth_url = linkedin.get_authorization_url()
        if auth_url:
            st.link_button("🔗 Conectar LinkedIn", auth_url, type="primary", use_container_width=True)
        else:
            st.error("⚠️ Credenciais não configuradas. Verifique os secrets.")
    
    st.markdown("---")
    st.markdown("### 🔑 Chaves de API")
    st.info("🚧 Em breve: Configure suas chaves de API do Gemini e NewsAPI.")

