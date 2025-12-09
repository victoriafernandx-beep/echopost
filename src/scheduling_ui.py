# Scheduling Page UI Component
# This file contains the complete scheduling interface
# To be inserted into app.py after the "Gerador de Posts" page

import streamlit as st
from src import database, scheduler
import datetime
import pytz

def render_scheduling_page(current_theme):
    """Render the complete scheduling page"""
    
    user_id = "test_user"  # Replace with actual user authentication
    
    # Hero Section
    st.markdown(f"""
    <div style='margin-bottom: 2rem;'>
        <h1 style='font-size: 2.25rem; margin-bottom: 0.5rem; color: {current_theme['deep_black']};'>
            📅 Agendamento de Posts
        </h1>
        <p style='font-size: 1rem; color: {current_theme['graphite']};'>
            Agende seus posts para publicação automática no LinkedIn
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📝 Agendar Novo Post", "📋 Posts Agendados", "🎯 Melhores Horários"])
    
    # ============================================
    # TAB 1: Schedule New Post
    # ============================================
    with tab1:
        st.markdown("### ✨ Criar e Agendar Post")
        
        # Option to use existing post or create new
        post_source = st.radio(
            "Origem do post:",
            ["📝 Escrever novo post", "📚 Usar post salvo"],
            horizontal=True
        )
        
        if post_source == "📝 Escrever novo post":
            # New post form
            with st.form("schedule_new_post"):
                topic = st.text_input(
                    "Tópico do post",
                    placeholder="Ex: Tendências de IA em 2025"
                )
                
                content = st.text_area(
                    "Conteúdo do post",
                    height=200,
                    placeholder="Escreva ou cole o conteúdo do seu post aqui..."
                )
                
                # Tags
                tags_input = st.text_input(
                    "Tags (separadas por vírgula)",
                    placeholder="ia, tecnologia, marketing"
                )
                
                st.markdown("---")
                st.markdown("#### ⏰ Quando publicar?")
                
                col_date, col_time, col_tz = st.columns([2, 1, 1])
                
                with col_date:
                    schedule_date = st.date_input(
                        "Data",
                        min_value=datetime.date.today(),
                        value=datetime.date.today() + datetime.timedelta(days=1)
                    )
                
                with col_time:
                    schedule_time = st.time_input(
                        "Horário",
                        value=datetime.time(9, 0)
                    )
                
                with col_tz:
                    timezone = st.selectbox(
                        "Fuso horário",
                        ["America/Sao_Paulo", "America/New_York", "Europe/London", "UTC"],
                        index=0
                    )
                
                # Preview scheduled time
                scheduled_datetime = datetime.datetime.combine(schedule_date, schedule_time)
                st.info(f"📅 Post será publicado em: **{scheduled_datetime.strftime('%d/%m/%Y às %H:%M')}** ({timezone})")
                
                submit = st.form_submit_button("📅 Agendar Post", type="primary", use_container_width=True)
                
                if submit:
                    if not content:
                        st.error("⚠️ Por favor, escreva o conteúdo do post!")
                    else:
                        # Convert to UTC for storage
                        local_dt = scheduled_datetime
                        utc_dt = scheduler.convert_to_utc(local_dt, timezone)
                        
                        # Parse tags
                        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
                        
                        # Create scheduled post
                        result = database.create_scheduled_post(
                            user_id=user_id,
                            content=content,
                            topic=topic or "Post agendado",
                            scheduled_time=utc_dt.isoformat(),
                            timezone=timezone,
                            tags=tags
                        )
                        
                        if result:
                            st.success("✅ Post agendado com sucesso!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Erro ao agendar post. Tente novamente.")
        
        else:
            # Use existing saved post
            st.markdown("#### 📚 Selecione um post salvo")
            
            saved_posts = database.get_posts(user_id, limit=20)
            
            if saved_posts:
                # Create a selectbox with post previews
                post_options = {}
                for post in saved_posts:
                    preview = post['content'][:60] + "..." if len(post['content']) > 60 else post['content']
                    post_options[f"{post['topic']} - {preview}"] = post
                
                selected_post_key = st.selectbox(
                    "Escolha um post:",
                    list(post_options.keys())
                )
                
                selected_post = post_options[selected_post_key]
                
                # Show post preview
                st.markdown("**Preview:**")
                st.markdown(f"""
                <div class="post-card">
                    <div class="post-topic">{selected_post['topic']}</div>
                    <div class="post-content">{selected_post['content']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Scheduling form
                with st.form("schedule_existing_post"):
                    st.markdown("#### ⏰ Quando publicar?")
                    
                    col_date, col_time, col_tz = st.columns([2, 1, 1])
                    
                    with col_date:
                        schedule_date = st.date_input(
                            "Data",
                            min_value=datetime.date.today(),
                            value=datetime.date.today() + datetime.timedelta(days=1)
                        )
                    
                    with col_time:
                        schedule_time = st.time_input(
                            "Horário",
                            value=datetime.time(9, 0)
                        )
                    
                    with col_tz:
                        timezone = st.selectbox(
                            "Fuso horário",
                            ["America/Sao_Paulo", "America/New_York", "Europe/London", "UTC"],
                            index=0
                        )
                    
                    scheduled_datetime = datetime.datetime.combine(schedule_date, schedule_time)
                    st.info(f"📅 Post será publicado em: **{scheduled_datetime.strftime('%d/%m/%Y às %H:%M')}** ({timezone})")
                    
                    submit = st.form_submit_button("📅 Agendar Post", type="primary", use_container_width=True)
                    
                    if submit:
                        # Convert to UTC
                        utc_dt = scheduler.convert_to_utc(scheduled_datetime, timezone)
                        
                        # Create scheduled post
                        result = database.create_scheduled_post(
                            user_id=user_id,
                            content=selected_post['content'],
                            topic=selected_post['topic'],
                            scheduled_time=utc_dt.isoformat(),
                            timezone=timezone,
                            tags=selected_post.get('tags', [])
                        )
                        
                        if result:
                            st.success("✅ Post agendado com sucesso!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Erro ao agendar post. Tente novamente.")
            else:
                st.info("📝 Você ainda não tem posts salvos. Crie um post primeiro!")
    
    # ============================================
    # TAB 2: Scheduled Posts List
    # ============================================
    with tab2:
        st.markdown("### 📋 Seus Posts Agendados")
        
        # Filter options
        col_filter1, col_filter2 = st.columns([2, 1])
        
        with col_filter1:
            status_filter = st.selectbox(
                "Filtrar por status:",
                ["pending", "published", "failed", "cancelled"],
                format_func=lambda x: {
                    "pending": "⏳ Pendentes",
                    "published": "✅ Publicados",
                    "failed": "❌ Falharam",
                    "cancelled": "🚫 Cancelados"
                }[x],
                index=0
            )
        
        with col_filter2:
            if st.button("🔄 Atualizar", use_container_width=True):
                st.rerun()
        
        # Get scheduled posts
        scheduled_posts = database.get_scheduled_posts(user_id, status=status_filter)
        
        if scheduled_posts:
            st.markdown(f"**{len(scheduled_posts)} posts encontrados**")
            st.markdown("---")
            
            for idx, post in enumerate(scheduled_posts):
                # Parse scheduled time
                try:
                    utc_time = datetime.datetime.fromisoformat(post['scheduled_time'].replace('Z', '+00:00'))
                    local_time = scheduler.convert_from_utc(utc_time, post.get('timezone', 'UTC'))
                    formatted_time = local_time.strftime('%d/%m/%Y às %H:%M')
                except:
                    formatted_time = post['scheduled_time']
                
                # Status badge
                status_colors = {
                    "pending": current_theme['warning'],
                    "published": current_theme['success'],
                    "failed": current_theme['error'],
                    "cancelled": current_theme['graphite']
                }
                status_icons = {
                    "pending": "⏳",
                    "published": "✅",
                    "failed": "❌",
                    "cancelled": "🚫"
                }
                
                status = post['status']
                status_color = status_colors.get(status, current_theme['graphite'])
                status_icon = status_icons.get(status, "❓")
                
                # Post card
                st.markdown(f"""
                <div class="post-card">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                        <div class="post-topic">{post['topic']}</div>
                        <span style="background: {status_color}15; color: {status_color}; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
                            {status_icon} {status.upper()}
                        </span>
                    </div>
                    <div style="color: {current_theme['graphite']}; font-size: 0.875rem; margin-bottom: 0.5rem;">
                        📅 Agendado para: <strong>{formatted_time}</strong> ({post.get('timezone', 'UTC')})
                    </div>
                    <div class="post-content">{post['content'][:200]}{'...' if len(post['content']) > 200 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col_actions = st.columns([1, 1, 1, 1, 4])
                
                with col_actions[0]:
                    if status == "pending":
                        if st.button("🗑️", key=f"cancel_{idx}", help="Cancelar"):
                            database.delete_scheduled_post(post['id'])
                            st.success("Post cancelado!")
                            st.rerun()
                
                with col_actions[1]:
                    if status == "pending":
                        if st.button("✏️", key=f"edit_{idx}", help="Reagendar"):
                            st.session_state[f'reschedule_{idx}'] = True
                
                with col_actions[2]:
                    if status == "failed":
                        if st.button("🔄", key=f"retry_{idx}", help="Tentar novamente"):
                            # Reschedule for 5 minutes from now
                            new_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
                            database.reschedule_post(post['id'], new_time.isoformat())
                            st.success("Post reagendado para daqui 5 minutos!")
                            st.rerun()
                
                with col_actions[3]:
                    if st.button("👁️", key=f"view_{idx}", help="Ver completo"):
                        with st.expander("Conteúdo completo", expanded=True):
                            st.markdown(post['content'])
                
                # Reschedule form (if edit button clicked)
                if st.session_state.get(f'reschedule_{idx}'):
                    with st.form(f"reschedule_form_{idx}"):
                        st.markdown("**Reagendar para:**")
                        
                        col_date, col_time = st.columns(2)
                        
                        with col_date:
                            new_date = st.date_input(
                                "Nova data",
                                min_value=datetime.date.today(),
                                key=f"new_date_{idx}"
                            )
                        
                        with col_time:
                            new_time = st.time_input(
                                "Novo horário",
                                key=f"new_time_{idx}"
                            )
                        
                        col_submit, col_cancel = st.columns(2)
                        
                        with col_submit:
                            if st.form_submit_button("✅ Confirmar", use_container_width=True):
                                new_datetime = datetime.datetime.combine(new_date, new_time)
                                utc_dt = scheduler.convert_to_utc(new_datetime, post.get('timezone', 'UTC'))
                                database.reschedule_post(post['id'], utc_dt.isoformat())
                                st.session_state[f'reschedule_{idx}'] = False
                                st.success("Post reagendado!")
                                st.rerun()
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                st.session_state[f'reschedule_{idx}'] = False
                                st.rerun()
                
                st.markdown("---")
        else:
            st.info(f"📭 Nenhum post {status_filter} encontrado.")
    
    # ============================================
    # TAB 3: Best Times Recommendations
    # ============================================
    with tab3:
        st.markdown("### 🎯 Melhores Horários para Postar")
        
        st.markdown(f"""
        <div style="background: {current_theme['soft_gray']}; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <p style="margin: 0; color: {current_theme['graphite']};">
                💡 Baseado na análise do seu histórico de posts e melhores práticas do LinkedIn
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get best posting times
        best_times = scheduler.get_best_posting_times(user_id, top_n=5)
        
        st.markdown("#### 🌟 Top 5 Horários Recomendados")
        
        for idx, recommendation in enumerate(best_times):
            confidence_pct = int(recommendation['confidence'] * 100)
            
            # Confidence color
            if confidence_pct >= 70:
                conf_color = current_theme['success']
            elif confidence_pct >= 50:
                conf_color = current_theme['warning']
            else:
                conf_color = current_theme['graphite']
            
            st.markdown(f"""
            <div class="post-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 600; color: {current_theme['deep_black']}; margin-bottom: 0.25rem;">
                            #{idx + 1} {recommendation['time_display']}
                        </div>
                        <div style="color: {current_theme['graphite']}; font-size: 0.875rem;">
                            {recommendation['reason']}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: {conf_color};">
                            {confidence_pct}%
                        </div>
                        <div style="font-size: 0.75rem; color: {current_theme['graphite']};">
                            confiança
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick schedule button
            if st.button(f"⚡ Agendar para {recommendation['time_display']}", key=f"quick_schedule_{idx}", use_container_width=True):
                st.session_state['quick_schedule_time'] = recommendation
                st.session_state['show_quick_schedule_form'] = True
                st.rerun()
        
        # Quick schedule form
        if st.session_state.get('show_quick_schedule_form'):
            st.markdown("---")
            st.markdown("### ⚡ Agendamento Rápido")
            
            recommended_time = st.session_state.get('quick_schedule_time')
            
            with st.form("quick_schedule_form"):
                content = st.text_area(
                    "Conteúdo do post",
                    height=150,
                    placeholder="Escreva seu post aqui..."
                )
                
                topic = st.text_input(
                    "Tópico (opcional)",
                    placeholder="Ex: Dicas de produtividade"
                )
                
                # Calculate next occurrence of recommended day/hour
                today = datetime.date.today()
                target_day = recommended_time['day_of_week']
                target_hour = recommended_time['hour']
                
                # Find next occurrence
                days_ahead = target_day - today.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                
                next_date = today + datetime.timedelta(days=days_ahead)
                next_datetime = datetime.datetime.combine(next_date, datetime.time(target_hour, 0))
                
                st.info(f"📅 Será agendado para: **{next_datetime.strftime('%d/%m/%Y às %H:%M')}**")
                
                col_submit, col_cancel = st.columns(2)
                
                with col_submit:
                    if st.form_submit_button("✅ Confirmar Agendamento", type="primary", use_container_width=True):
                        if content:
                            utc_dt = scheduler.convert_to_utc(next_datetime, "America/Sao_Paulo")
                            
                            result = database.create_scheduled_post(
                                user_id=user_id,
                                content=content,
                                topic=topic or "Post agendado",
                                scheduled_time=utc_dt.isoformat(),
                                timezone="America/Sao_Paulo",
                                tags=[]
                            )
                            
                            if result:
                                st.success("✅ Post agendado com sucesso!")
                                st.session_state['show_quick_schedule_form'] = False
                                st.balloons()
                                st.rerun()
                        else:
                            st.error("⚠️ Por favor, escreva o conteúdo do post!")
                
                with col_cancel:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        st.session_state['show_quick_schedule_form'] = False
                        st.rerun()
        
        # Statistics section
        st.markdown("---")
        st.markdown("### 📊 Estatísticas de Agendamento")
        
        # Get counts
        pending_count = database.get_scheduled_posts_count(user_id, "pending")
        published_count = database.get_scheduled_posts_count(user_id, "published")
        failed_count = database.get_scheduled_posts_count(user_id, "failed")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⏳ Pendentes", pending_count)
        
        with col2:
            st.metric("✅ Publicados", published_count)
        
        with col3:
            st.metric("❌ Falharam", failed_count)
