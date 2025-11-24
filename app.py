import streamlit as st
from src import database
from src import generator

st.set_page_config(
    page_title="EchoPost",
    page_icon="📢",
    layout="wide"
)

st.title("📢 EchoPost")
st.subheader("Sua plataforma de criação de conteúdo para LinkedIn com IA")

st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para", ["Home", "Gerador de Posts", "News Radar", "Configurações"])

if page == "Home":
    st.write("Bem-vindo ao EchoPost! Use o menu lateral para navegar.")
    
    # Display recent posts
    st.subheader("Seus Posts Recentes")
    # Simulate a user ID for now
    user_id = "test_user"
    posts = database.get_posts(user_id)
    
    if posts:
        for post in posts:
            with st.expander(f"{post.get('topic', 'Sem tópico')} - {post.get('created_at', '')}"):
                st.write(post.get('content'))
    else:
        st.info("Nenhum post encontrado. Vá ao Gerador de Posts para criar um!")


elif page == "Gerador de Posts":
    st.header("Gerador de Conteúdo")
    st.header("Gerador de Conteúdo")
    
    topic = st.text_input("Sobre o que você quer escrever?")
    if st.button("Gerar Post"):
        if topic:
            content = generator.generate_post(topic)
            st.session_state['last_post'] = content
            st.session_state['last_topic'] = topic
            st.success("Post gerado!")
        else:
            st.warning("Por favor, insira um tópico.")
            
    if 'last_post' in st.session_state:
        st.text_area("Conteúdo Gerado", st.session_state['last_post'], height=200)
        
        if st.button("Salvar no Banco de Dados"):
            user_id = "test_user" # Mock user
            result = database.create_post(user_id, st.session_state['last_post'], st.session_state['last_topic'])
            if result:
                st.success("Post salvo com sucesso!")
            else:
                st.error("Erro ao salvar. Verifique se a tabela 'posts' existe no Supabase.")

elif page == "News Radar":
    st.header("📡 News Radar")
    st.write("Em breve: Notícias relevantes para o seu setor.")

elif page == "Configurações":
    st.header("Configurações")
    st.write("Em breve: Gerencie sua conta e chaves de API.")
