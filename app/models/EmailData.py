from typing import List, TypedDict

class EmailData(TypedDict):
    """Tipo que representa um email retornado via IMAP"""
    id: str
    subject: str
    sender: str
    date: str
    labels: List[str]
    snippet: str