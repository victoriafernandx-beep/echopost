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
    page_title="EchoPost",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, premium look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Main title styling */
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(255, 255, 255, 0.8);
        animation: slideUp 0.6s ease-out;
    }

    
    .post-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: slideUp 0.4s ease-out;
    }
    
    .post-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
    }
    
    .post-meta {
        color: #666;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    
    .post-topic {
        color: #667eea;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .post-content {
        color: #333;
        line-height: 1.6;
        margin: 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        transform: scale(1.01);
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    .char-counter {
        text-align: right;
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .char-counter.warning {
        color: #ff6b6b;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    
    /* Template card styling */
    .template-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border: 2px solid #e0e0e0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .template-card:hover {
        border-color: #667eea;
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
</style>
""", unsafe_allow_html=True)


st.title("📢 EchoPost")
st.markdown("### Sua plataforma de criação de conteúdo para LinkedIn com IA")

st.sidebar.title("🧭 Navegação")
page = st.sidebar.radio("Ir para", ["🏠 Home", "✨ Gerador de Posts", "📡 News Radar", "⚙️ Configurações"])

# Dark mode toggle
st.sidebar.markdown("---")
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False

# Better dark mode toggle
col_icon, col_toggle = st.sidebar.columns([1, 3])
with col_icon:
    if st.session_state['dark_mode']:
        st.markdown("### 🌙")
    else:
        st.markdown("### ☀️")
with col_toggle:
    dark_mode = st.toggle("Modo Escuro" if not st.session_state['dark_mode'] else "Modo Claro", 
                          value=st.session_state['dark_mode'], 
                          key="theme_toggle")
    
if dark_mode != st.session_state['dark_mode']:
    st.session_state['dark_mode'] = dark_mode
    st.rerun()

# Apply dark mode CSS if enabled
if st.session_state['dark_mode']:
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }
        .post-card {
            background: rgba(30, 30, 30, 0.95) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        .post-topic {
            color: #8b9aff !important;
        }
        .post-content {
            background: #2a2a2a !important;
            color: #e0e0e0 !important;
        }
        .post-meta {
            color: #aaa !important;
        }
    </style>
    """, unsafe_allow_html=True)

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
    
    st.markdown("## 👋 Bem-vindo ao EchoPost!")
    
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
        <div class="post-card" style="text-align: center;">
            <div style="color: #667eea; font-size: 0.9rem; margin-bottom: 0.5rem;">👥 Seguidores</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1a1a1a;">{metrics['followers']:,}</div>
            <div style="color: #10b981; font-size: 0.85rem; margin-top: 0.5rem;">↑ {metrics['followers_change']} ({metrics['followers_percent']})</div>
            <div style="color: #666; font-size: 0.75rem;">vs período anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="post-card" style="text-align: center;">
            <div style="color: #667eea; font-size: 0.9rem; margin-bottom: 0.5rem;">👁️ Impressões</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1a1a1a;">{metrics['impressions']:,}</div>
            <div style="color: #10b981; font-size: 0.85rem; margin-top: 0.5rem;">↑ {metrics['impressions_change']}</div>
            <div style="color: #666; font-size: 0.75rem;">vs período anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="post-card" style="text-align: center;">
            <div style="color: #667eea; font-size: 0.9rem; margin-bottom: 0.5rem;">💬 Engajamento</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1a1a1a;">{metrics['engagement']}%</div>
            <div style="color: #10b981; font-size: 0.85rem; margin-top: 0.5rem;">↑ {metrics['engagement_change']}</div>
            <div style="color: #666; font-size: 0.75rem;">vs período anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="post-card" style="text-align: center;">
            <div style="color: #667eea; font-size: 0.9rem; margin-bottom: 0.5rem;">📝 Posts</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1a1a1a;">{metrics['total_posts']}</div>
            <div style="color: #10b981; font-size: 0.85rem; margin-top: 0.5rem;">↑ {metrics['posts_change']}</div>
            <div style="color: #666; font-size: 0.75rem;">vs período anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Insights Section
    st.markdown("### 💡 Insights Automáticos")
    insights = analytics.get_insights(metrics)
    
    cols_insights = st.columns(len(insights))
    for idx, insight in enumerate(insights):
        with cols_insights[idx]:
            bg_color = "#d1fae5" if insight['type'] == "positive" else "#fef3c7" if insight['type'] == "tip" else "#dbeafe"
            text_color = "#065f46" if insight['type'] == "positive" else "#92400e" if insight['type'] == "tip" else "#1e40af"
            
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 1rem; border-radius: 8px; height: 100%;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{insight['icon']}</div>
                <div style="font-weight: 600; color: {text_color}; margin-bottom: 0.25rem;">{insight['title']}</div>
                <div style="font-size: 0.85rem; color: {text_color};">{insight['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two columns: Popular Posts and Engagement Chart
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### 📊 Publicações mais populares da semana")
        
        popular_posts = analytics.get_popular_posts()
        
        # Convert to DataFrame for better display
        import pandas as pd
        df = pd.DataFrame(popular_posts)
        df.columns = ['Post', 'Impressões', 'Comentários', 'Salvamentos', 'Taxa Eng.']
        
        # Style the dataframe
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Post": st.column_config.TextColumn("Post", width="medium"),
                "Impressões": st.column_config.NumberColumn("Impressões", format="%d"),
                "Comentários": st.column_config.NumberColumn("Comentários"),
                "Salvamentos": st.column_config.NumberColumn("Salvamentos"),
                "Taxa Eng.": st.column_config.TextColumn("Taxa Eng.")
            }
        )

    
    with col_right:
        st.markdown("### 📈 Engajamento (30 dias)")
        
        dates, engagement = analytics.get_engagement_chart_data()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=engagement,
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=6, color='#764ba2'),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
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
                title="Taxa (%)"
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
            
            col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
            with col1:
                if st.button("🗑️ Deletar", key=f"del_{idx}"):
                    database.delete_post(post_id)
                    st.rerun()
            with col2:
                if st.button(f"{'⭐' if not is_favorite else '☆'} Favorito", key=f"fav_{idx}"):
                    database.toggle_favorite(post_id, not is_favorite)
                    st.rerun()
            with col3:
                # Tag editor
                new_tags = st.multiselect(
                    "Tags",
                    options=all_tags + ["+ Nova tag"],
                    default=post_tags,
                    key=f"tags_{idx}",
                    label_visibility="collapsed"
                )
                
                # Handle new tag creation
                if "+ Nova tag" in new_tags:
                    new_tags.remove("+ Nova tag")
                    new_tag = st.text_input("Nova tag:", key=f"new_tag_{idx}", placeholder="Digite a nova tag")
                    if new_tag and st.button("Adicionar", key=f"add_tag_{idx}"):
                        new_tags.append(new_tag)
                        database.update_post_tags(post_id, new_tags)
                        st.rerun()
                elif new_tags != post_tags:
                    if st.button("💾 Salvar tags", key=f"save_tags_{idx}"):
                        database.update_post_tags(post_id, new_tags)
                        st.success("Tags atualizadas!")
                        st.rerun()
            
            with col4:
                if st.button("📋 Copiar", key=f"copy_{idx}"):
                    st.code(content, language=None)
                    st.success("Conteúdo exibido acima para copiar!")
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
    
    col1, col2 = st.columns([2, 1])

    
    with col1:
        topic = st.text_input("💡 Sobre o que você quer escrever?", placeholder="Ex: Inteligência Artificial no mercado de trabalho")
    
    with col2:
        tone = st.selectbox("🎭 Tom do post", ["Profissional", "Casual", "Inspiracional"])
    
    if st.button("🚀 Gerar Post", use_container_width=True):
        if topic:
            with st.spinner("✨ Gerando seu post..."):
                content = generator.generate_post(topic, tone)
                st.session_state['last_post'] = content
                st.session_state['last_topic'] = topic
                st.success("✅ Post gerado com sucesso!")
                st.balloons()
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
                    if st.button(tag, key=f"tag_{idx}", use_container_width=True):
                        if tag not in content:
                            st.session_state['last_post'] = content + " " + tag
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
            <div style="max-width: 375px; margin: 0 auto; background: #000; border-radius: 40px; padding: 15px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
                <div style="background: #000; height: 30px; border-radius: 0 0 20px 20px; margin: -15px -15px 10px -15px;"></div>
                <div style="background: white; border-radius: 8px; overflow: hidden; min-height: 500px;">
                    <div style="padding: 12px; border-bottom: 1px solid #e0e0e0; display: flex; align-items: center; justify-content: space-between;">
                        <div style="color: #0a66c2; font-weight: bold; font-size: 18px;">in</div>
                        <div style="color: #666; font-size: 12px;">Feed</div>
                    </div>
                    <div style="padding: 12px;">
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <div style="width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 18px; margin-right: 8px;">U</div>
                            <div style="flex: 1;">
                                <div style="font-weight: 600; color: #000; font-size: 14px;">Seu Nome</div>
                                <div style="font-size: 12px; color: #666;">Seu cargo</div>
                                <div style="font-size: 11px; color: #666;">Agora • 🌐</div>
                            </div>
                        </div>
                        <div style="color: #000; line-height: 1.5; white-space: pre-wrap; word-wrap: break-word; font-size: 14px;">{content}</div>
                        <div style="display: flex; justify-content: space-around; padding-top: 8px; margin-top: 12px; border-top: 1px solid #e0e0e0;">
                            <div style="color: #666; font-size: 13px;">👍 Curtir</div>
                            <div style="color: #666; font-size: 13px;">💬 Comentar</div>
                            <div style="color: #666; font-size: 13px;">🔄 Compartilhar</div>
                        </div>
                    </div>
                </div>
                <div style="background: #fff; height: 5px; width: 134px; border-radius: 100px; margin: 10px auto 0;"></div>
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
                    st.balloons()
                else:
                    st.error("❌ Erro ao salvar.")

        
        with col2:
            from src import linkedin
            if linkedin.is_connected():
                if st.button("🔗 Publicar no LinkedIn", use_container_width=True):
                    success, message = linkedin.post_to_linkedin(content)
                    if success:
                        st.success(message)
                        st.balloons()
                    else:
                        st.error(message)
            else:
                st.info("Conecte o LinkedIn nas Configurações")
        
        with col3:
            if st.button("📋 Copiar para Clipboard", use_container_width=True):
                st.code(content, language=None)
                st.info("👆 Copie o texto acima!")


elif page == "📡 News Radar":
    st.markdown("## 📡 News Radar")
    st.info("🚧 Em breve: Notícias relevantes para o seu setor com geração automática de posts!")

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
            # Debug info
            creds = linkedin.get_linkedin_credentials()
            st.caption(f"🔍 Debug: Redirect URI sendo usada: `{creds['redirect_uri']}`")
            st.caption("Certifique-se que esta URL está EXATAMENTE igual no LinkedIn Developers > Auth > Redirect URLs")
        else:
            st.error("⚠️ Credenciais não configuradas. Verifique os secrets.")
    
    st.markdown("---")
    st.markdown("### 🔑 Chaves de API")
    st.info("🚧 Em breve: Configure suas chaves de API do Gemini e NewsAPI.")

