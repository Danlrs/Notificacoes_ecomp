
<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=3B6790&height=120&section=header"/>

<h1 align="center">Sistema de Notificações Inteligente</h1>

<div align="center">  
  <img width=40% src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=EFB036&style=for-the-badge"/>
</div>

<h3 align="center">Colegiado de Engenharia de Computação - UEFS</h3>

<p align="center">Sistema web que captura, classifica automaticamente e organiza e-mails do colegiado de Engenharia de Computação da UEFS, permitindo que estudantes busquem e filtrem mensagens por categorias de interesse.</p>

## 🎯 Objetivo do Projeto

O objetivo principal é **facilitar o acesso dos estudantes a informações relevantes** enviadas pelo colegiado, utilizando **classificação automática por filtros** para organizar e-mails em 13 categorias. Os alunos podem buscar e filtrar e-mails de acordo com suas necessidades, sem perder avisos importantes em caixas de entrada lotadas.

**🌐 Acesse a aplicação:** https://projeto-de-extensao-sigma.vercel.app/

## ⚙️ Funcionalidades Principais

### 📧 Captura e Classificação Automática
- **Conexão IMAP** com Gmail para leitura de e-mails do colegiado
- **Sistema de filtros** para classificação automática
- **11 categorias:** Achados e Perdidos, Prováveis Concluintes/Formandos, Avisos da Coordenação/Secretaria, Estágio/Trainee/Oportunidades, TCC/Projeto Final, Pesquisa/Iniciação Científica/Pós-Graduação, Monitoria/Tutoria/Bolsas Acadêmicas, Eventos/Palestras/Workshops, Disciplinas/Professores/Aulas, Matrícula/Ajuste de Disciplina/SEI, Assistência Estudantil/Benefícios, e Outros
- **Verificação periódica** automática (configurável)

### 🔍 Sistema de Busca e Filtros
- **Barra de pesquisa** para localizar e-mails específicos
- **Filtros por categoria** para visualização organizada
- **Visualização de todos os e-mails** ou por categoria específica
- **Interface responsiva** (desktop e mobile)

<details>
  <summary><b>🛠 Tecnologias</b></summary>

## 🛠 Tecnologias

### Backend
1. **Python 3.13+**
2. **Flask** (API REST)
3. **IMAP** (captura de e-mails)
4. **Sistema de filtros** (classificação)
5. **APScheduler** (verificação periódica)

### Frontend
1. **HTML5 / CSS3 / JavaScript**
2. **Design responsivo**
3. **Interface moderna** e intuitiva

### Infraestrutura
1. **Vercel** (deploy)
2. **Banco de dados** estruturado

</details>

<details>
  <summary><b>✔️ Pré-requisitos</b></summary>

## ✔️ Pré-requisitos
- Python 3.8+
- Conta Gmail (para receber e-mails)
- Senha de App do Google (16 caracteres)
- Navegador moderno (Chrome, Firefox, Edge)

</details>

<details>
  <summary><b>🔐 Configuração da Senha de App do Gmail</b></summary>

## 🔐 Configuração da Senha de App do Gmail

### 1. Ative a Verificação em 2 Etapas
1. Acesse: https://myaccount.google.com/security
2. Clique em "Verificação em duas etapas"
3. Siga as instruções para ativar

### 2. Gere uma Senha de App
1. Acesse: https://myaccount.google.com/apppasswords
2. Selecione **"Email"** como app
3. Selecione **"Outro (nome personalizado)"** como dispositivo
4. Digite: `Sistema Notificações ECOMP`
5. Clique em **"Gerar"**
6. **Copie a senha de 16 caracteres** (formato: `abcd efgh ijkl mnop`)

### 3. Configure no .env
- **Remova os espaços** ao colar no arquivo `.env`
- Exemplo: `GMAIL_PASSWORD=abcdefghijklmnop`

</details>

<details>
  <summary><b>💻 Instruções para Rodar o Projeto Localmente</b></summary>

## 💻 Instruções para Rodar o Projeto Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/Danlrs/Notificacoes_ecomp.git
cd Notificacoes_ecomp
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`
Crie um arquivo `.env` na raiz do projeto:

```bash
# ============================================
# CONFIGURAÇÃO DE EMAIL (IMAP)
# ============================================

# Email que RECEBE os emails do colegiado (sua conta)
GMAIL_RECIPIENT=seu.email@gmail.com

# Senha de App do Gmail (16 caracteres SEM ESPAÇOS!)
GMAIL_PASSWORD=abcdefghijklmnop

# Email que ENVIA os emails (do colegiado)
GMAIL_SENDER=ccecomp@ecomp.uefs.br

# ============================================
# CONFIGURAÇÕES DO SERVIDOR
# ============================================

# Intervalo de verificação (minutos)
CHECK_EMAILS_INTERVAL_MINUTES=5

# API InboxStream (se aplicável)
INBOXSTREAM_API_URL=
```

### 5. Teste a conexão com Gmail
```bash
python app/services/gmail_imap.py
```
Deve exibir: `✅ Conectado com sucesso!`

### 6. Inicie o servidor
```bash
python main.py
```

### 7. Acesse no navegador
Abra: http://localhost:5000

</details>

<details>
  <summary><b>🧪 Testando o Sistema</b></summary>

## 🧪 Testando o Sistema

### Adicionar E-mail de Teste (PowerShell)
```powershell
$body = @{
    subject = "Processo seletivo de estágio na Petrobras"
    labels = @("Oportunidades")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/admin/add-email" -Method POST -Body $body -ContentType "application/json; charset=utf-8"
```

### Buscar E-mails
1. Acesse http://localhost:5000
2. Use a barra de pesquisa para localizar e-mails específicos
3. Filtre por categoria usando os botões de filtro
4. Visualize todos os e-mails ou apenas de uma categoria específica

</details>

<details>
  <summary><b>📋 Categorias Disponíveis</b></summary>

## 📋 Categorias de E-mails (11 tipos)

| # | Categoria |
|---|-----------|
| 1 | **Todos** |
| 2 | **Achados e Perdidos** |
| 3 | **Prováveis Concluintes / Formandos** |
| 4 | **Avisos da Coordenação / Secretaria** |
| 5 | **Estágio / Trainee / Oportunidades** |
| 6 | **TCC / Projeto Final** |
| 7 | **Pesquisa / Iniciação Científica / Pós-Graduação** |
| 8 | **Monitoria / Tutoria / Bolsas Acadêmicas** |
| 9 | **Eventos / Palestras / Workshops** |
| 10 | **Disciplinas / Professores / Aulas** |
| 11 | **Matrícula / Ajuste de Disciplina / SEI** |
| 12 | **Assistência Estudantil / Benefícios** |
| 13 | **Outros** |

</details>

<details>
  <summary><b>🚀 Deploy na Vercel</b></summary>

## 🚀 Deploy na Vercel

O projeto está hospedado na Vercel e pode ser acessado em:
**https://projeto-de-extensao-sigma.vercel.app/**

### Configuração de Variáveis de Ambiente
No painel da Vercel, configure as seguintes variáveis:
- `GMAIL_RECIPIENT`
- `GMAIL_PASSWORD`
- `GMAIL_SENDER`
- `CHECK_EMAILS_INTERVAL_MINUTES`
- `INBOXSTREAM_API_URL` (se aplicável)

</details>

## 📊 Estrutura do Projeto

```
Notificacoes_ecomp/
├── app/
│   ├── api/
│   │   └── inbox_stream.py         # API de captura de e-mails
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py             # Configurações do projeto
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── models/
│   │   ├── EmailData.py            # Modelo de dados de e-mail
│   │   ├── __init__.py
│   │   └── base.py
│   ├── services/
│   │   ├── EmailClassifer.py       # Classificador de e-mails
│   │   └── gmail_imap.py           # Serviço IMAP
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── views/
│       ├── __init__.py
│       └── base.py
├── __init__.py
├── .env.example                    # Exemplo de configurações
├── .gitignore
├── main.py                         # Arquivo principal
├── README.md
└── requirements.txt                # Dependências Python
```

## 💻 Desenvolvedores
 
<table>
  <tr>

<td align="center"><a href="https://github.com/alexsami-lopes" target="_blank"><img style="" src="https://avatars.githubusercontent.com/u/103523809?v=4" width="100px;" alt=""/><br /><sub><b> Alexsami Lopes </b></sub></a><br />👨🏻‍💻</a></td>
<td align="center"><a href="https://github.com/Danlrs" target="_blank"><img style="" src="https://avatars.githubusercontent.com/u/94250524?v=4" width="100px;" alt=""/><br /><sub><b> Daniel Lucas </b></sub></a><br />👨🏻‍💻</a></td>
<td align="center"><a href="https://github.com/icaroo-oliveira" target="_blank"><img style="" src="https://avatars.githubusercontent.com/u/143228771?v=4" width="100px;" alt=""/><br /><sub><b> Ícaro Oliveira </b></sub></a><br />👩🏾‍💻</a></td>
<td align="center"><a href="https://github.com/luanbsc" target="_blank"><img style="" src="https://avatars.githubusercontent.com/u/113149444?v=4" width="100px;" alt=""/><br /><sub><b> Luan Barbosa </b></sub></a><br />👨🏻‍💻</a></td>
<td align="center"><a href="https://github.com/silascosta" target="_blank"><img style="" src="https://avatars.githubusercontent.com/u/66216800?v=4" width="100px;" alt=""/><br /><sub><b> Silas Costa </b></sub></a><br />👩🏾‍💻</a></td>
<td align="center"><a href="https://github.com/ThiagoSenaJT" target="_blank"><img style="" src="https://avatars.githubusercontent.com/u/194796433?v=4" width="100px;" alt=""/><br /><sub><b> Thiago Sena </b></sub></a><br />👨🏻‍💻</a></td>


  </tr>
</table>

## 📄 Licença

Este projeto está sob a licença MIT.

---

<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=3B6790&height=120&section=footer"/>
