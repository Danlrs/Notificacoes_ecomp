# importações padrão do Python
import re
import unicodedata
from typing import List, Dict

# Importações de arquivos internos
from app.models.EmailData import EmailData


class EmailClassifier:
    """
    Classificador simples de emails baseado em palavras-chave,
    com priorização inteligente e correspondência por palavras inteiras.
    """

    def __init__(self):
        # Ordem de prioridade — categorias mais importantes primeiro
        self.category_order: List[str] = [
            "Achados e Perdidos",
            "Prováveis Concluintes / Formandos",
            "Avisos da Coordenação / Secretaria",
            "Estágio / Trainee / Oportunidades",
            "TCC / Projeto Final",
            "Pesquisa / Iniciação Científica / Pós-Graduação",
            "Monitoria / Tutoria / Bolsas Acadêmicas",
            "Eventos / Palestras / Workshops",
            "Disciplinas / Professores / Aulas",
            "Matrícula / Ajuste de Disciplina / SEI",
            "Assistência Estudantil / Benefícios",
            "Outros"
        ]

        # Palavras-chave por categoria
        self.categories: Dict[str, List[str]] = {
            "Avisos da Coordenação / Secretaria": [
                "coordenacao", "ccecomp", "secretaria", "comunicado", "aviso",
                "documento", "prazo", "formulario", "calendario", "cancelamento",
                "solicitacao", "publicacao", "eleicao", "colegiado", "coordenador",
                "vice coordenador", "gestao", "convocacao", "comissao"
            ],
            "TCC / Projeto Final": [
                "tcc", "trabalho de conclusao", "banca", "orientador",
                "projeto final", "defesa", "monografia", "resumo", "correcao",
                "apresentacao"
            ],
            "Prováveis Concluintes / Formandos": [
                "provaveis concluintes", "formando", "formandos", "colacao de grau",
                "banco de talentos", "egresso", "egressos", "finalista",
                "ultimo semestre", "conclusao do curso"
            ],
            "Estágio / Trainee / Oportunidades": [
                "estagio", "trainee", "vaga", "emprego", "oportunidade",
                "recrutamento", "bolsa", "curriculo", "contratacao",
                "processo seletivo", "empresa"
            ],
            "Pesquisa / Iniciação Científica / Pós-Graduação": [
                "pesquisa", "pibic", "ic", "iniciacao cientifica", "laboratorio",
                "submissao", "artigo", "paper", "publicacao", "pos graduacao",
                "mestrado", "doutorado"
            ],
            "Disciplinas / Professores / Aulas": [
                "aula", "professor", "disciplina", "nota", "atividade", "prova",
                "trabalho", "avaliacao", "materiais", "cancelada", "reposicao",
                "horario"
            ],
            "Eventos / Palestras / Workshops": [
                "palestra", "seminario", "evento", "oficina", "workshop", "encontro",
                "congresso", "simposio", "mesa redonda", "live", "webinar", "feira"
            ],
            "Monitoria / Tutoria / Bolsas Acadêmicas": [
                "monitoria", "tutoria", "bolsa", "inscricao", "edital", "resultado",
                "aprovado", "selecionado", "auxilio", "substituto"
            ],
            "Assistência Estudantil / Benefícios": [
                "assistencia", "bolsa", "auxilio", "moradia", "alimentacao",
                "transporte", "beneficio", "proae", "cadastro", "socioeconomico"
            ],
            "Matrícula / Ajuste de Disciplina / SEI": [
                "matricula", "ajuste", "cancelamento", "sei", "inscricao", "reajuste",
                "trancamento", "historico", "periodo", "disciplina", "cadastro"
            ],
            "Achados e Perdidos": [
                "achado", "achados", "perdido", "perdidos", "achados e perdidos",
                "objeto encontrado", "objeto perdido", "encontrado", "perdi"
            ],
            "Outros": []
        }

    def normalize_text(self, text: str) -> str:
        """Remove acentos e pontuação, e converte para minúsculas"""
        text = text.lower()
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        return text

    def contains_keyword(self, text: str, keyword: str) -> bool:
        """Verifica se a palavra-chave aparece isolada (palavra inteira)"""
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return re.search(pattern, text) is not None

    def classify_email(self, email: EmailData) -> str:
        """Classifica um único email com base no assunto e snippet"""
        subject = self.normalize_text(email.get("subject", ""))
        snippet = self.normalize_text(email.get("snippet", ""))
        full_text = subject + " " + snippet

        matches: Dict[str, int] = {}

        for category, keywords in self.categories.items():
            count = sum(1 for kw in keywords if self.contains_keyword(full_text, kw))
            if count > 0:
                matches[category] = count

        if not matches:
            return "Outros"

        # Critério: mais correspondências, depois prioridade
        best_category = max(
            matches,
            key=lambda c: (matches[c], -self.category_order.index(c))
        )
        return best_category

    def classify_all(self, emails: List[EmailData]) -> List[EmailData]:
        """Classifica uma lista de emails e adiciona o campo 'categoria'"""
        classified: List[EmailData] = []
        for email in emails:
            categoria = self.classify_email(email)
            email_with_cat = email.copy()
            email_with_cat["categoria"] = categoria  # adiciona a categoria dinamicamente
            classified.append(email_with_cat)
        return classified
