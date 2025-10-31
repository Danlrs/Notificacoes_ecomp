#!/usr/bin/env python3
"""
Aplicação principal do sistema de notificações
"""
# Importações padrão do Python
import os
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
        print(f"[{categoria}] {e['subject']}")
        # print(f"De: {e['sender']}")
        # print(f"Prévia: {e['snippet'][:80]}...\n")

def main():
    """Função principal da aplicação"""
    # get_emails() # Descomente para testar a obtenção e classificação de emails
    pass

if __name__ == "__main__":
    main()
