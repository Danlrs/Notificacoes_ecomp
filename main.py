#!/usr/bin/env python3
"""
Aplicação principal do sistema de notificações
"""
# Importações padrão do Python
import os
import time
from typing import List
from dotenv import load_dotenv

# --- Força o Python a usar a pasta raiz do script como diretório de trabalho ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)
# ----------------

# Importações de módulos internos
from app.services.gmail_imap import fetch_unread_emails
from app.services.EmailClassifer import EmailClassifier
from app.models.EmailData import EmailData
from app.api.inbox_stream import send_email_to_api

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.gmail_imap import fetch_unread_emails
from app.services.EmailClassifer import EmailClassifier
from app.api.inbox_stream import send_email_to_api
import os
import time
from dotenv import load_dotenv
from threading import Thread
from typing import List

app = FastAPI(
    title="InboxStream API",
    version="v1",
    description="API para ingestão, categorização e notificação em tempo real de e-mails."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega variáveis de ambiente
load_dotenv()

def get_emails():
    """Função para obter emails classificados"""
    emails: List[EmailData] = fetch_unread_emails(max_results=2, unread_only=True)
    classifier = EmailClassifier()
    classificados: List[EmailData] = classifier.classify_all(emails)
    print("\n📂 Emails classificados:\n")
    for e in classificados:
        categoria = e.get("categoria", "Outros")
        try:
            send_email_to_api(e)
        except Exception as ex:
            print(f"❌ Falha ao enviar email ID {e['id']} para API: {ex}")
            continue
        print(f"[{categoria}] {e['subject']}")
        # print(f"De: {e['sender']}")
        # print(f"Prévia: {e['snippet'][:80]}...\n")

def watch_emails(poll_interval_seconds: int = 300):
    """Polling: busca emails a cada poll_interval_seconds (padrão 300s = 5min)"""
    print(f"⏱️  Iniciando polling: a cada {poll_interval_seconds} segundos. (Ctrl+C para parar)\n")
    try:
        while True:
            get_emails()
            time.sleep(poll_interval_seconds)
    except KeyboardInterrupt:
        print("\n⛔ Polling interrompido pelo usuário. Saindo...")

def main():
    """Função principal da aplicação"""
    # Inicia polling a cada 1 minuto
    watch_emails(poll_interval_seconds=60)
    pass

@app.on_event("startup")
async def startup_event():
    """Inicia o serviço de polling em uma thread separada"""
    print("🚀 Iniciando o serviço de polling...")
    thread = Thread(target=get_emails)
    thread.start()

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "InboxStream API is running!"}

# Para rodar: uvicorn app:app --reload