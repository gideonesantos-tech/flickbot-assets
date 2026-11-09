import os
import time
import random
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Cole sua URL gerada no Workflows do Teams aqui (ou use variável de ambiente)
WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL", "https://defaultb4741a826b6e43a5ad6e1044511aae.d6.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/24/workflows/03d2947a340f4dce8f3666ded2c61b79/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=n5mToMsf3O3Zf_Vr-Q6qEg5Zz4z4zqmQodcUuQR5SHA")

# URL base onde ficam as fotos profissionais da equipe (ajuste para o domínio/repositório de vocês)
BASE_FOTO_URL = "https://raw.githubusercontent.com/Unicamp-E-Racing/assets/main/fotos/"

# ==============================================================================
# BANCO DE DADOS DOS 66 MEMBROS (EXTRAÍDO DO PDF DA EQUIPE)
# ==============================================================================
MEMBROS = [
    # Página 1
    {"nome": "Felipe Petrillo Fici Zackiewicz", "apelido": "Fici", "data": "29/10", "foto": ""},
    {"nome": "Cairê Belo da Silva", "apelido": "Cairê", "data": "06/12", "foto": ""},
    {"nome": "Igor Dela Costa de Oliveira", "apelido": "Igor", "data": "27/12", "foto": ""},
    {"nome": "Guilherme Souza", "apelido": "Mogli", "data": "02/02", "foto": ""},
    {"nome": "Pedro Jaluul Cardo", "apelido": "Jalulu", "data": "01/05", "foto": ""},
    {"nome": "Pedro Campanha Neto", "apelido": "Pedro Campanha", "data": "23/12", "foto": ""},
    {"nome": "Paulo Rodrigues de Oliveira Nilo", "apelido": "Paulo Rodrigues", "data": "03/05", "foto": ""},
    {"nome": "Maria Clara de Araújo Bianchi", "apelido": "Maria", "data": "17/05", "foto": ""},
    {"nome": "Davi Roldão Siqueira", "apelido": "Davi", "data": "05/06", "foto": ""},
    {"nome": "Ana Beatriz Alves Chammas", "apelido": "Chammas", "data": "13/10", "foto": ""},
    {"nome": "Daniel Abraão de Brito Nogueira", "apelido": "Daniel", "data": "23/10", "foto": ""},
    {"nome": "Artur Dias de Oliveira", "apelido": "Artur", "data": "27/11", "foto": ""},
    {"nome": "Jéssica Ramos dos Santos", "apelido": "Jéssica", "data": "13/12", "foto": ""},
    {"nome": "Paulo Vitor Figueiredo da Silva", "apelido": "Paulo Vitor", "data": "20/12", "foto": ""},
    {"nome": "Mateus Silva Cirino", "apelido": "Teteu", "data": "14/01", "foto": ""},
    {"nome": "Rodolfo Yoon Sang Joo", "apelido": "Rodolfera", "data": "03/02", "foto": ""},
    {"nome": "Arthur Tsuyoshi Nakaza Nanaumi", "apelido": "Nanaumi", "data": "16/02", "foto": ""},
    {"nome": "João Pedro Kwecko Guimarães", "apelido": "Kwecko", "data": "14/04", "foto": ""},
    {"nome": "Guilherme Lubito Dutra", "apelido": "ADM", "data": "06/05", "foto": ""},
    {"nome": "Ana Luísa Marzinotti Francisco", "apelido": "Ana Chico", "data": "21/05", "foto": ""},
    # Página 2
    {"nome": "Wallace Dametto Teixeira", "apelido": "Wallace", "data": "01/06", "foto": ""},
    {"nome": "Felipe Santos Mendonça", "apelido": "Felipe", "data": "19/07", "foto": ""},
    {"nome": "Anna Julia Filigoi", "apelido": "Anna", "data": "27/07", "foto": ""},
    {"nome": "Letícia da Costa Venancio", "apelido": "Letuca", "data": "04/08", "foto": ""},
    {"nome": "Mateus Cardoso Santos", "apelido": "Manga", "data": "05/10", "foto": ""},
    {"nome": "Sophia Garcia Sousa", "apelido": "Sophia", "data": "20/11", "foto": ""},
    {"nome": "Eduardo Kobata Marto", "apelido": "Kobata", "data": "18/12", "foto": ""},
    {"nome": "Bruno Soares Alves", "apelido": "Cap", "data": "30/01", "foto": ""},
    {"nome": "Helena Prandini Mandl", "apelido": "Helena", "data": "22/03", "foto": ""},
    {"nome": "Victor Antonio Moraes Pimenta", "apelido": "Pepper", "data": "10/04", "foto": ""},
    {"nome": "Pedro Henrique Pereira Valadão", "apelido": "Baladinha", "data": "12/05", "foto": ""},
    {"nome": "Gabriel Luiz Patara Buiocchi", "apelido": "Salsicha", "data": "17/05", "foto": ""},
    {"nome": "Fernanda Matsumoto Lima", "apelido": "Fernandinha", "data": "27/05", "foto": ""},
    {"nome": "Pedro de Carvalho Ferreira", "apelido": "Pedro Carvalho", "data": "25/06", "foto": ""},
    {"nome": "Giovana Dioz Recio", "apelido": "Gi", "data": "07/07", "foto": ""},
    {"nome": "João Vitor Castelo Branco Diniz", "apelido": "Bolinha", "data": "26/07", "foto": ""},
    {"nome": "Leonardo Ferreira", "apelido": "Leleo", "data": "04/08", "foto": ""},
    {"nome": "André Mendes de Almeida Lima", "apelido": "Tijolo", "data": "06/08", "foto": ""},
    {"nome": "Luíza Lima Lattuf", "apelido": "Luíza", "data": "03/09", "foto": ""},
    {"nome": "Arthur Ryu Miyashiro", "apelido": "Hamadinha", "data": "05/09", "foto": ""},
    # Página 3
    {"nome": "Lucas Rodrigues Hirashima", "apelido": "Hirashima", "data": "02/10", "foto": ""},
    {"nome": "Alcenor Guimarães Barbosa", "apelido": "Alcenoia", "data": "16/10", "foto": ""},
    {"nome": "Pedro Viveiros Lopes", "apelido": "Chuchu", "data": "22/10", "foto": ""},
    {"nome": "Beatriz Aimi Ramos Umetsu", "apelido": "Babubia", "data": "16/12", "foto": ""},
    {"nome": "Rafael Levi Siqueira de Andrade", "apelido": "Levi", "data": "31/12", "foto": ""},
    {"nome": "Felipe Pigari Gonçalves", "apelido": "Pigari", "data": "01/01", "foto": ""},
    {"nome": "Arthur Tsuzuki Morita", "apelido": "Makita", "data": "01/01", "foto": ""},
    {"nome": "Leonardo Tetsuo Moura Hamada", "apelido": "Hamada", "data": "08/01", "foto": ""},
    {"nome": "Gregório Wernke", "apelido": "Gregório", "data": "16/01", "foto": ""},
    {"nome": "Raphael Batarce Momenté", "apelido": "Rapha", "data": "01/03", "foto": ""},
    {"nome": "João Gabriel Iuzviak Mantagute", "apelido": "Mantagute", "data": "24/03", "foto": ""},
    {"nome": "Gabriel Farias De Marco", "apelido": "McLovin", "data": "02/04", "foto": ""},
    {"nome": "Enrico Turazza Miraldo", "apelido": "Enrico", "data": "04/04", "foto": ""},
    {"nome": "Gustavo Pires Ximenes", "apelido": "Ximene", "data": "02/05", "foto": ""},
    {"nome": "Gabriel de Andrade Gomes", "apelido": "Gabriel", "data": "21/05", "foto": ""},
    {"nome": "Augusto Maciel Guedes", "apelido": "Augusto", "data": "18/07", "foto": ""},
    {"nome": "Pedro Takeshi Suzuki", "apelido": "CEO", "data": "25/07", "foto": ""},
    {"nome": "Lucas Pace Zerbinatti", "apelido": "Pace (leia como quiser)", "data": "24/09", "foto": ""},
    {"nome": "Isabelle Tenorio", "apelido": "Belle", "data": "02/10", "foto": ""},
    {"nome": "Hari Kharlus Arthur Khāna Tolentino", "apelido": "Hari", "data": "19/10", "foto": ""},
    # Página 4
    {"nome": "Vítor Souza Mendes da Silva", "apelido": "Vitin", "data": "01/11", "foto": ""},
    {"nome": "Maria Clara Nunes Luz da Costa", "apelido": "Nunes", "data": "30/12", "foto": ""},
    {"nome": "Matheus Andrade Theophilo", "apelido": "Vamp", "data": "10/01", "foto": ""},
    {"nome": "Isabely Ruppel", "apelido": "Ruppel", "data": "14/03", "foto": ""},
    {"nome": "Luis Felipe Azzalin Ukon", "apelido": "Zara", "data": "24/03", "foto": ""},
    {"nome": "Rafael Francisco Coutinho Neto", "apelido": "Rafael", "data": "06/06", "foto": ""},
]

# ==============================================================================
# FRASES E INTRODUÇÕES AUTÊNTICAS DO FLICKBOT (ESTILO OFICINA / ATAS)
# ==============================================================================
INTRODUCOES_DIA = [
    "🐜 **Bom dia, formiguinhas!** O dia de hoje começa com o aniversário de uma pessoa muito especial em nossa equipe!",
    "🐜 **Acorda, formigueiro!** São 06h30 da manhã, a Jetson ainda não caiu e hoje o dia começa em festa na oficina!",
    "🏎️ **Bom dia, formiguinhas da E-Racing!** Larguem as ferramentas por um segundo porque o calendário do FlickBot apitou!",
    "⚡ **Bora acordar, formiguinhas!** Mais um dia de correria no projeto, mas hoje temos um motivo extra para comemorar!",
    "🔧 **Bom dia, formigueiro!** Nem só de solda duvidosa e ata de reunião vive esta equipe. Hoje é dia de festa!"
]

MENSAGENS_SUSPENSE_SINGULAR = [
    "Quem será que está ficando mais velho(a) hoje e já pode pagar uma pizza pra oficina inteira? 👀",
    "Preparando os arquivos confidenciais do Gerador de Atas... Achamos o(a) aniversariante do dia! 🥁",
    "Diz a lenda que quem faz aniversário hoje ganha isenção de limpar a oficina (mentira, não ganha não, mas ganha parabéns)! 🎉"
]

MENSAGENS_SUSPENSE_PLURAL = [
    "E hoje não é aniversário em dose única não! Passar na E-Racing é igual atacado: você olha o calendário de hoje e leva aniversariante em dobro! 👀🎉",
    "O formigueiro hoje está em festa múltipla! Segura a sequência de aniversariantes do dia! 🥁🔥"
]

# Frases próprias do FlickBot inspiradas diretamente nas pérolas das Atas da oficina
FRASES_FLICKBOT_OFICINA = [
    '"Confesso que essa solda ficou duvidosa, mas o seu aniversário ficou 10/10! Parabéns, {apelido}!" — FlickBot, 2026',
    '"Não sou o Lucas, mas estou no meio do formigueiro só pra te dar parabéns, {apelido}!" — FlickBot',
    '"A gente tem quase a mesma porcentagem de água que uma melancia. O que muda é que hoje o(a) {apelido} tem bolo e ansiedade!" — FlickBot',
    '"Se tudo der errado na oficina hoje, é porque era pra dar... menos o aniversário do(a) {apelido}! Taca no Gepeto e comemora!" — FlickBot',
    '"O próximo que falar que o aniversário do(a) {apelido} é plug-and-play vai levar um tapa! Hoje o dia é todo seu!" — FlickBot',
    '"Tá tudo dando errado mas tudo bem, hoje tem aniversário do(a) {apelido} (e esperamos que tenha pizza)!" — FlickBot',
    '"Codar com a mente, debugar com o coração e comemorar o aniversário do(a) {apelido} na oficina sem moderação!" — FlickBot',
    '"Até lá, se tiver que dobrar um main hoop num poste pra comemorar o aniversário do(a) {apelido}, a gente vai dobrar!" — FlickBot',
    '"A gente não precisa ter tudo na oficina, mas o parabéns do(a) {apelido} tem que ser o melhor!" — FlickBot',
    '"Quem diria que o fabricante estava certo quando lançou o(a) {apelido} no mundo! Mais um ano de garantia renovado!" — FlickBot',
    '"Não tem como fazer engenharia e esquecer o aniversário do(a) {apelido}! Parabéns, lenda!" — FlickBot',
    '"Aura não se explica, se sente — e hoje a aura do formigueiro tá todinha no aniversário do(a) {apelido}!" — FlickBot',
    '"Na de você não querer se meter, você já fez mais um ano de vida na E-Racing! Parabéns, {apelido}!" — FlickBot',
    '"Eu surto mas logo me volto, ainda mais pra dar feliz aniversário pro(a) {apelido} às 6h30 da manhã!" — FlickBot'
]


# ==============================================================================
# FUNÇÕES DE ENVIO PARA O MICROSOFT TEAMS (ADAPTIVE CARDS)
# ==============================================================================
def enviar_card_teams(blocos_body):
    """Envia um Adaptive Card formatado para a URL de Webhook/Workflows do Teams."""
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": blocos_body
                }
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=payload, timeout=15)
    response.raise_for_status()


def enviar_texto_simples(texto):
    """Envia um balão de mensagem de texto no chat do Teams."""
    blocos = [
        {
            "type": "TextBlock",
            "text": texto,
            "wrap": True,
            "size": "Medium"
        }
    ]
    enviar_card_teams(blocos)


def enviar_card_aniversariante(membro):
    """Envia o card completo do aniversariante com Foto, Nome, Apelido e Frase do FlickBot."""
    frase_sorteada = random.choice(FRASES_FLICKBOT_OFICINA).format(
        apelido=membro["apelido"],
        nome=membro["nome"]
    )
    
    # Se não tiver URL de foto cadastrada ainda, gera avatar elegante com as iniciais
    apelido_url = requests.utils.quote(membro["apelido"])
    foto_url = membro["foto"] if membro["foto"] else f"https://ui-avatars.com/api/?name={apelido_url}&background=D32F2F&color=fff&size=256&bold=true"

    blocos = [
        {
            "type": "TextBlock",
            "text": f"🎂 FELIZ ANIVERSÁRIO, {membro['apelido'].upper()}! 🎉",
            "weight": "Bolder",
            "size": "Large",
            "color": "Attention",
            "wrap": True
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": foto_url,
                            "size": "Large",
                            "style": "Person"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "stretch",
                    "verticalContentAlignment": "Center",
                    "items": [
                        {
                            "type": "FactSet",
                            "facts": [
                                {"title": "Nome Completo:", "value": membro["nome"]},
                                {"title": "Apelido na Oficina:", "value": membro["apelido"]},
                                {"title": "Data:", "value": membro["data"]}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "type": "Container",
            "style": "emphasis",
            "bleed": True,
            "items": [
                {
                    "type": "TextBlock",
                    "text": "💬 **Pérola de Aniversário do FlickBot:**",
                    "weight": "Bolder",
                    "size": "Small",
                    "wrap": True
                },
                {
                    "type": "TextBlock",
                    "text": f"*{frase_sorteada}*",
                    "wrap": True,
                    "isSubtle": True
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": f"Mandem os parabéns aqui no chat para o(a) **{membro['apelido']}**! 🐜🏎️⚡",
            "wrap": True,
            "weight": "Bolder"
        }
    ]
    enviar_card_teams(blocos)


# ==============================================================================
# LÓGICA PRINCIPAL DE EXECUÇÃO ÀS 06H30
# ==============================================================================
def executar_flickbot():
    fuso_br = ZoneInfo("America/Sao_Paulo")
    hoje = datetime.now(fuso_br)
    amanha = hoje + timedelta(days=1)

    str_hoje = hoje.strftime("%d/%m")
    str_amanha = amanha.strftime("%d/%m")

    aniversariantes_hoje = [m for m in MEMBROS if m["data"] == str_hoje]
    aniversariantes_amanha = [m for m in MEMBROS if m["data"] == str_amanha]

    # Busca também aniversariantes em datas muito próximas (daqui a 2 ou 3 dias)
    proximos_dias = []
    for delta in (2, 3):
        data_futura = (hoje + timedelta(days=delta)).strftime("%d/%m")
        for m in MEMBROS:
            if m["data"] == data_futura:
                proximos_dias.append((m, delta))

    # 1. SEQUÊNCIA DE ANIVERSARIANTES DO DIA
    if aniversariantes_hoje:
        # Mensagem 1: Bom dia formiguinhas (Introdução)
        enviar_texto_simples(random.choice(INTRODUCOES_DIA))
        time.sleep(3)

        # Mensagem 2: Suspense (adapta singular ou plural)
        if len(aniversariantes_hoje) == 1:
            enviar_texto_simples(random.choice(MENSAGENS_SUSPENSE_SINGULAR))
        else:
            enviar_texto_simples(random.choice(MENSAGENS_SUSPENSE_PLURAL))
        time.sleep(3)

        # Mensagem 3+: Card individual para cada aniversariante do dia
        for membro in aniversariantes_hoje:
            enviar_card_aniversariante(membro)
            time.sleep(3)

    # 2. AVISO DE 1 DIA ANTES (VÉSPERA)
    if aniversariantes_amanha:
        if not aniversariantes_hoje:
            enviar_texto_simples(
                "🐜 **Bom dia, formiguinhas!** Passando às 06h30 com o radar do **FlickBot** ligado!"
            )
            time.sleep(3)

        nomes_amanha = ", ".join(
            [f"**{m['nome']} ({m['apelido']})**" for m in aniversariantes_amanha]
        )
        enviar_texto_simples(
            f"🚨 **ALERTA DE VÉSPERA DO FLICKBOT:** Amanhã ({str_amanha}) é dia de aniversário na equipe! "
            f"Já preparem os parabéns (e o bolo na oficina) para: {nomes_amanha}! 🎈👀"
        )
        time.sleep(2)

    # 3. RADAR DE DATAS PRÓXIMAS (QUANDO HÁ ANIVERSÁRIO HOJE OU AMANHÃ E OUTROS COLADOS)
    if (aniversariantes_hoje or aniversariantes_amanha) and proximos_dias:
        lista_prox = ", ".join(
            [f"**{m['apelido']}** ({m['data']} - daqui a {d} dias)" for m, d in proximos_dias]
        )
        enviar_texto_simples(
            f"📅 **Combo de Aniversários da Semana:** Fiquem ligados que logo na sequência também temos: {lista_prox}!"
        )


if __name__ == "__main__":
    executar_flickbot()
