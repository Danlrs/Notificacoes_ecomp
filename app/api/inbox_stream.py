import json
from typing import Dict, List
from email.utils import parsedate_to_datetime
import datetime
import requests

API_URL = "http://localhost:8000/api/v1/emails"
TIMEOUT_SECONDS = 6


def _to_iso_utc(date_str: str) -> str:
    """Converte header Date para ISO UTC; se falhar, usa agora UTC"""
    try:
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt.astimezone(datetime.timezone.utc).isoformat()
    except Exception:
        return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()


def build_payload(email: Dict) -> Dict:
    """
    Normaliza um dicionário de email para o schema da API:
    {
      "id": "string",
      "subject": "string",
      "body": "string",
      "category": "Geral",
      "date": "2025-11-16T13:30:39.557Z"
    }
    """
    return {
        "id": str(email.get("id") or email.get("message_id") or ""),
        "subject": email.get("subject", ""),
        "body": email.get("body") or email.get("snippet", "") or "",
        "category": email.get("category", "Geral"),
        "date": _to_iso_utc(email.get("date", ""))
    }


def send_email_to_api(email: Dict) -> bool:
    """Envia um email (um objeto) para a API. Retorna True se 2xx."""
    payload = build_payload(email)
    try:
        resp = requests.post(API_URL, json=payload, timeout=TIMEOUT_SECONDS)
        if 200 <= resp.status_code < 300:
            return True
        else:
            # opcional: log curto em stderr/console
            print(f"⚠️  API retornou {resp.status_code}: {resp.text}")
            return False
    except requests.RequestException as e:
        print(f"❌ Erro ao enviar para API: {e}")
        raise e


def send_batch_to_api(emails: List[Dict]) -> Dict[str, bool]:
    """Envia vários emails; retorna mapa id->sucesso"""
    results = {}
    for e in emails:
        eid = str(e.get("id", "")) or "<no-id>"
        ok = send_email_to_api(e)
        results[eid] = ok
    return results