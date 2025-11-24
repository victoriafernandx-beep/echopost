import streamlit as st
from src import database
from src import generator
import datetime

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
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
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
    }
</style>
""", unsafe_allow_html=True)

st.title("📢 EchoPost")
st.markdown("### Sua plataforma de criação de conteúdo para LinkedIn com IA")

st.sidebar.title("🧭 Navegação")
page = st.sidebar.radio("Ir para", ["🏠 Home", "✨ Gerador de Posts", "📡 News Radar", "⚙️ Configurações"])

# Dark mode toggle
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Tema")
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False

dark_mode = st.sidebar.toggle("🌙 Modo Escuro", value=st.session_state['dark_mode'])
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
    
    # Metrics Cards
    metrics = analytics.get_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="post-card" style="text-align: center;">
            <div style="color: #667eea; font-size: 0.9rem; margin-bottom: 0.5rem;">👥 Seguidores</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1a1a1a;">{metrics['followers']:,}</div>
            <div style="color: #10b981; font-size: 0.85rem; margin-top: 0.5rem;">↑ {metrics['followers_change']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="post-card" style="text-align: center;">
            <div style="color: #667eea; font-size: 0.9rem; margin-bottom: 0.5rem;">👁️ Impressões (7d)</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1a1a1a;">{metrics['impressions']:,}</div>
            <div style="color: #10b981; font-size: 0.85rem; margin-top: 0.5rem;">↑ {metrics['impressions_change']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="post-card" style="text-align: center;">
            <div style="color: #667eea; font-size: 0.9rem; margin-bottom: 0.5rem;">💬 Engajamento</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1a1a1a;">{metrics['engagement']}%</div>
            <div style="color: #10b981; font-size: 0.85rem; margin-top: 0.5rem;">↑ {metrics['engagement_change']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="post-card" style="text-align: center;">
            <div style="color: #667eea; font-size: 0.9rem; margin-bottom: 0.5rem;">📝 Posts</div>
            <div style="font-size: 2rem; font-weight: 700; color: #1a1a1a;">{metrics['total_posts']}</div>
            <div style="color: #10b981; font-size: 0.85rem; margin-top: 0.5rem;">↑ {metrics['posts_change']}</div>
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
    
    # Recent Posts Section
    st.markdown("### 📝 Seus Posts Recentes")
    
    user_id = "test_user"
    posts = database.get_posts(user_id)
    
    if posts:
        for idx, post in enumerate(posts):
            topic = post.get('topic', 'Sem tópico')
            content = post.get('content', '')
            created_at = post.get('created_at', '')
            post_id = post.get('id')
            
            # Format date
            try:
                date_obj = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%d/%m/%Y às %H:%M')
            except:
                formatted_date = created_at
            
            # Create card
            st.markdown(f"""
            <div class="post-card">
                <div class="post-topic">{topic}</div>
                <div class="post-meta">📅 {formatted_date} • {len(content)} caracteres</div>
                <div class="post-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("🗑️ Deletar", key=f"del_{idx}"):
                    database.delete_post(post_id)
                    st.rerun()
            with col2:
                if st.button("📋 Copiar", key=f"copy_{idx}"):
                    st.code(content, language=None)
                    st.success("Conteúdo exibido acima para copiar!")
    else:
        st.info("🎯 Nenhum post encontrado. Vá ao Gerador de Posts para criar um!")


elif page == "✨ Gerador de Posts":
    from src import ai_helpers
    
    st.markdown("## ✨ Gerador de Conteúdo")
    
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
            st.markdown("### 👁️ Preview LinkedIn")
            
            # LinkedIn-style preview card
            st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 1.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="
                        width: 48px;
                        height: 48px;
                        border-radius: 50%;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-weight: bold;
                        font-size: 1.2rem;
                        margin-right: 0.75rem;
                    ">U</div>
                    <div>
                        <div style="font-weight: 600; color: #000;">Seu Nome</div>
                        <div style="font-size: 0.85rem; color: #666;">Seu cargo • LinkedIn</div>
                        <div style="font-size: 0.75rem; color: #666;">Agora</div>
                    </div>
                </div>
                <div style="
                    color: #000;
                    line-height: 1.6;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                ">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Salvar no Banco de Dados", use_container_width=True):
                user_id = "test_user"
                result = database.create_post(user_id, content, st.session_state['last_topic'])
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
        
        if st.button("🔗 Conectar LinkedIn"):
            if linkedin.connect_linkedin():
                st.success("✅ LinkedIn conectado com sucesso!")
                st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔑 Chaves de API")
    st.info("🚧 Em breve: Configure suas chaves de API do Gemini e NewsAPI.")

