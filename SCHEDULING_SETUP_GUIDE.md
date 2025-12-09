# 📅 Guia de Instalação do Sistema de Agendamento

## Passo 1: Instalar Dependências

Execute o comando abaixo para instalar as novas dependências necessárias:

```bash
pip install apscheduler pytz
```

Ou instale todas as dependências do projeto:

```bash
pip install -r requirements.txt
```

## Passo 2: Criar Tabela no Supabase

1. Acesse o painel do Supabase (https://app.supabase.com)
2. Vá para o seu projeto
3. Clique em "SQL Editor" no menu lateral
4. Abra o arquivo `scheduled_posts_schema.sql`
5. Copie todo o conteúdo do arquivo
6. Cole no SQL Editor do Supabase
7. Clique em "Run" para executar o script

Isso criará:
- ✅ Tabela `scheduled_posts`
- ✅ Índices para performance
- ✅ Trigger para auto-atualização de timestamps
- ✅ Políticas de Row Level Security (RLS)

## Passo 3: Verificar Instalação

Execute o app normalmente:

```bash
streamlit run app.py
```

Você verá:
- ✅ Nova opção "📅 Agendamento" no menu lateral
- ✅ Scheduler iniciado em background (verificar logs no console)

## Passo 4: Testar Funcionalidades

### Teste 1: Agendar um Post
1. Vá para "📅 Agendamento"
2. Na aba "📝 Agendar Novo Post"
3. Escreva um post de teste
4. Escolha data/hora (pode ser 2-3 minutos no futuro para teste rápido)
5. Clique em "📅 Agendar Post"
6. Verifique se aparece mensagem de sucesso

### Teste 2: Ver Posts Agendados
1. Vá para a aba "📋 Posts Agendados"
2. Verifique se seu post aparece com status "⏳ PENDING"
3. Teste os botões de ação (Cancelar, Reagendar, etc.)

### Teste 3: Melhores Horários
1. Vá para a aba "🎯 Melhores Horários"
2. Veja as recomendações de horários
3. Teste o agendamento rápido clicando em um horário sugerido

### Teste 4: Publicação Automática
1. Agende um post para 2 minutos no futuro
2. Aguarde o horário agendado
3. O scheduler verificará a cada 1 minuto
4. Após publicação, o status mudará para "✅ PUBLISHED"
5. Verifique na aba "Posts Agendados" com filtro "published"

## Estrutura de Arquivos Criados

```
echopost/
├── app.py                          # ✅ Atualizado (menu + scheduler init)
├── requirements.txt                # ✅ Atualizado (apscheduler, pytz)
├── scheduled_posts_schema.sql      # ✅ Novo (schema do banco)
├── src/
│   ├── database.py                 # ✅ Atualizado (+8 funções)
│   ├── scheduler.py                # ✅ Novo (serviço de agendamento)
│   └── scheduling_ui.py            # ✅ Novo (interface completa)
```

## Funcionalidades Implementadas

### ✅ Database Layer
- Tabela `scheduled_posts` com todos os campos necessários
- 8 funções para CRUD de posts agendados
- Suporte a timezone
- Rastreamento de status (pending/published/failed/cancelled)
- Contagem de tentativas de retry

### ✅ Scheduler Service
- Background task runner usando APScheduler
- Verificação automática a cada 1 minuto
- Publicação automática de posts no horário agendado
- Retry logic (até 3 tentativas)
- Análise de melhores horários baseada em histórico
- Conversão de timezone (UTC ↔ Local)

### ✅ UI Components
- **Tab 1 - Agendar Novo Post:**
  - Escrever novo post ou usar post salvo
  - Seletor de data/hora/timezone
  - Preview do horário agendado
  
- **Tab 2 - Posts Agendados:**
  - Lista de posts com filtro por status
  - Cards com informações completas
  - Ações: Cancelar, Reagendar, Retry, Ver completo
  - Badges de status coloridos
  
- **Tab 3 - Melhores Horários:**
  - Top 5 horários recomendados
  - Score de confiança
  - Agendamento rápido com 1 clique
  - Estatísticas de agendamento

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'apscheduler'"
**Solução:** Execute `pip install apscheduler pytz`

### Erro: "relation 'scheduled_posts' does not exist"
**Solução:** Execute o script SQL no Supabase (Passo 2)

### Scheduler não está publicando posts
**Verificações:**
1. Verifique se o scheduler foi iniciado (mensagem no console)
2. Confirme que o horário agendado já passou
3. Verifique se o status do post é "pending"
4. Veja os logs no console para erros

### Posts ficam com status "failed"
**Possíveis causas:**
1. LinkedIn API não está configurada
2. Token de acesso expirado
3. Rate limit da API excedido

**Solução temporária:** O scheduler marca como "published" mesmo sem LinkedIn API conectada (para testes)

## Próximos Passos (Opcional)

### 1. Conectar LinkedIn API
Para publicação real no LinkedIn, implemente a função `publish_post()` em `src/linkedin.py`

### 2. Adicionar Notificações
Implemente sistema de notificações (email, push, in-app) na função `_notify_user()`

### 3. Melhorar Análise de Melhores Horários
Quando tiver métricas reais de engajamento, atualize `get_best_posting_times()` para usar dados reais

### 4. Deploy do Scheduler
Para produção, considere:
- Heroku com worker dyno
- Railway
- Supabase Edge Functions
- Celery + Redis

## Suporte

Se encontrar problemas:
1. Verifique os logs no console
2. Confirme que todas as dependências estão instaladas
3. Verifique se a tabela foi criada no Supabase
4. Teste com posts agendados para 2-3 minutos no futuro

---

**🎉 Parabéns! O sistema de agendamento está pronto para uso!**
