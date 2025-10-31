"""
Integração SIMPLES com Gmail usando IMAP
Requer apenas: email + senha de app (16 caracteres)
"""

# Importações padrão do Python
import os
import imaplib
import email
from email.header import decode_header
from typing import List

# Importações de arquivos internos
from app.models.EmailData import EmailData

# Carrega variáveis de ambiente

class GmailIMAPReader:
    def __init__(self):
        """
        Inicializa leitor Gmail via IMAP
        Credenciais vêm do arquivo .env
        """
        self.email_address = os.getenv('GMAIL_RECIPIENT')
        self.password = os.getenv('GMAIL_PASSWORD')
        self.sender_filter = os.getenv('GMAIL_SENDER', 'ccecomp@ecomp.uefs.br')
        self.imap = None
        
        if not self.email_address or not self.password:
            print("❌ Erro: Configure GMAIL_RECIPIENT e GMAIL_PASSWORD no .env")
            return
        
        print(f"📧 Email configurado: {self.email_address}")
        print(f"🔍 Filtrando emails de: {self.sender_filter}")
        
        self.connect()
    
    def connect(self):
        """Conecta ao Gmail via IMAP"""
        try:
            print("\n⏳ Conectando ao Gmail...")
            
            # Conecta ao servidor IMAP do Gmail
            self.imap = imaplib.IMAP4_SSL('imap.gmail.com')
            
            # Faz login
            self.imap.login(self.email_address, self.password)
            
            print("✅ Conectado com sucesso!")
            return True
            
        except imaplib.IMAP4.error as e:
            print(f"❌ Erro ao autenticar: {e}")
            print("\n📋 Verifique:")
            print("   1. Email e senha estão corretos no .env")
            print("   2. Senha de App foi gerada (não use a senha normal)")
            print("   3. Verificação em 2 etapas está ativada")
            print("\n💡 Gerar senha de app: https://myaccount.google.com/apppasswords")
            return False
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False
    
    def get_emails_from_sender(self, sender_email=None, max_results=10, unread_only=False):
        """
        Busca emails de um remetente específico
        
        Args:
            sender_email: Email do remetente (usa GMAIL_SENDER do .env se None)
            max_results: Número máximo de emails
            unread_only: Se True, busca apenas não lidos
        
        Returns:
            Lista de dicionários com dados dos emails
        """
        if not self.imap:
            print("❌ Não conectado ao Gmail")
            return []
        
        if sender_email is None:
            sender_email = self.sender_filter
        
        try:
            # Seleciona a caixa de entrada
            self.imap.select('INBOX')
            
            # Monta critério de busca
            if unread_only:
                search_criteria = f'(FROM "{sender_email}" UNSEEN)'
            else:
                search_criteria = f'(FROM "{sender_email}")'
            
            print(f"\n🔍 Buscando: {search_criteria}")
            
            # Busca emails
            status, messages = self.imap.search(None, search_criteria)
            
            if status != 'OK':
                print("❌ Erro ao buscar emails")
                return []
            
            # IDs dos emails encontrados
            email_ids = messages[0].split()
            
            if not email_ids:
                print("   Nenhum email encontrado")
                return []
            
            # Limita ao máximo solicitado (pega os mais recentes)
            email_ids = email_ids[-max_results:]
            
            print(f"   Encontrados: {len(email_ids)} emails")
            
            emails = []
            
            # Processa cada email
            for email_id in reversed(email_ids):  # Mais recentes primeiro
                email_data = self.get_email_details(email_id)
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except Exception as e:
            print(f"❌ Erro ao buscar emails: {e}")
            return []
    
    def get_email_details(self, email_id):
        """
        Extrai detalhes de um email específico
        
        Args:
            email_id: ID do email no servidor
        
        Returns:
            Dicionário com dados do email
        """
        try:
            # Busca o email
            status, msg_data = self.imap.fetch(email_id, '(RFC822)')
            
            if status != 'OK':
                return None
            
            # Parseia o email
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extrai assunto
            subject = self.decode_header_value(msg.get('Subject', ''))
            
            # Extrai remetente
            sender = self.decode_header_value(msg.get('From', ''))
            
            # Extrai data
            date_str = msg.get('Date', '')
            
            # Extrai labels/flags (Gmail via IMAP usa X-GM-LABELS)
            labels = []
            if msg.get('X-GM-LABELS'):
                labels = msg.get('X-GM-LABELS').split()
            
            # Extrai prévia do corpo
            snippet = self.get_email_body(msg, preview_only=True)
            
            return {
                'id': email_id.decode() if isinstance(email_id, bytes) else str(email_id),
                'subject': subject,
                'sender': sender,
                'date': date_str,
                'labels': labels,
                'snippet': snippet[:200]  # Primeiros 200 caracteres
            }
            
        except Exception as e:
            print(f"⚠️  Erro ao processar email {email_id}: {e}")
            return None
    
    def decode_header_value(self, header_value):
        """Decodifica header do email (lida com encoding)"""
        if not header_value:
            return ""
        
        decoded_parts = decode_header(header_value)
        decoded_string = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_string += part.decode(encoding or 'utf-8', errors='ignore')
                except:
                    decoded_string += part.decode('utf-8', errors='ignore')
            else:
                decoded_string += str(part)
        
        return decoded_string
    
    def get_email_body(self, msg, preview_only=True):
        """
        Extrai corpo do email
        
        Args:
            msg: Objeto email.message
            preview_only: Se True, retorna apenas prévia (segurança)
        
        Returns:
            Texto do email
        """
        body = ""
        
        try:
            # Email pode ter múltiplas partes (multipart)
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    
                    # Procura por texto simples
                    if content_type == "text/plain":
                        try:
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode('utf-8', errors='ignore')
                                break
                        except:
                            continue
            else:
                # Email simples (não-multipart)
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
            
            # Se for apenas prévia, retorna primeiros caracteres
            if preview_only and body:
                body = body[:500]  # Primeiros 500 caracteres
            
            return body.strip()
            
        except Exception as e:
            print(f"⚠️  Erro ao extrair corpo: {e}")
            return ""
    
    def mark_as_read(self, email_id):
        """Marca email como lido"""
        try:
            self.imap.store(email_id, '+FLAGS', '\\Seen')
            return True
        except Exception as e:
            print(f"⚠️  Erro ao marcar como lido: {e}")
            return False
    
    def get_labels(self):
        """Lista todas as labels/pastas disponíveis"""
        try:
            status, folders = self.imap.list()
            
            if status == 'OK':
                print("\n📁 Pastas/Labels disponíveis:")
                for folder in folders:
                    print(f"   {folder.decode()}")
            
            return folders
        except Exception as e:
            print(f"❌ Erro ao listar pastas: {e}")
            return []
    
    def disconnect(self):
        """Desconecta do Gmail"""
        try:
            if self.imap:
                self.imap.logout()
                print("👋 Desconectado do Gmail")
        except:
            pass


def fetch_unread_emails(max_results: int = 5, unread_only: bool = True) -> List[EmailData]:
    """
    Lê emails não lidos de um remetente específico configurado no .env
    
    Args:
        max_results: número máximo de emails a retornar
    
    Returns:
        Lista de dicionários com informações dos emails
    """
    gmail = GmailIMAPReader()

    if not gmail.imap:
        print("❌ Falha na conexão. Configure o .env corretamente.")
        return []

    emails: List[EmailData] = gmail.get_emails_from_sender(
        max_results=max_results,
        unread_only=unread_only
    )

    gmail.disconnect()

    return emails
