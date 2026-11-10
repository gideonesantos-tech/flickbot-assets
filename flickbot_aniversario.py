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
    {"nome": "Felipe Petrillo Fici Zackiewicz", "apelido": "Fici", "data": "29/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/fici_sorrindo.jpg"},
    {"nome": "Cairê Belo da Silva", "apelido": "Cairê", "data": "06/12", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/caire_sorrindo.png"},
    {"nome": "Igor Dela Costa de Oliveira", "apelido": "Igor", "data": "10/11", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/igor_sorrindo.png"},
    {"nome": "Guilherme Souza", "apelido": "Mogli", "data": "02/02", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/guilherme_sorrindo.png"},
    {"nome": "Pedro Jaluul Cardo", "apelido": "Jalulu", "data": "01/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/jaluul_sorrindo.png"},
    {"nome": "Pedro Campanha Neto", "apelido": "Pedro Campanha", "data": "23/12", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/pedro_campanha_sorrindo.png"},
    {"nome": "Paulo Rodrigues de Oliveira Nilo", "apelido": "Paulo Rodrigues", "data": "03/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/paulo_sorrindo.png"},
    {"nome": "Maria Clara de Araújo Bianchi", "apelido": "Maria", "data": "17/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/maria_bianchi_sorrindo.png"},
    {"nome": "Davi Roldão Siqueira", "apelido": "Davi", "data": "05/06", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/davi_sorrindo.png"},
    {"nome": "Ana Beatriz Alves Chammas", "apelido": "Chammas", "data": "13/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/ana_chammas_sorrindo.png"},
    {"nome": "Daniel Abraão de Brito Nogueira", "apelido": "Daniel", "data": "23/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/daniel_sorrindo.png"},
    {"nome": "Artur Dias de Oliveira", "apelido": "Artur", "data": "27/11", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/artur_oliveira_sorrindo.png"},
    {"nome": "Jéssica Ramos dos Santos", "apelido": "Jéssica", "data": "13/12", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/jessica_sorrindo.png"},
    {"nome": "Paulo Vitor Figueiredo da Silva", "apelido": "Paulo Vitor", "data": "20/12", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/paulo_vitor_sorrindo.png"},
    {"nome": "Mateus Silva Cirino", "apelido": "Teteu", "data": "14/01", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/mateus_cirino_sorrindo.png"},
    {"nome": "Rodolfo Yoon Sang Joo", "apelido": "Rodolfera", "data": "03/02", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/rodolfo_sorrindo.png"},
    {"nome": "Arthur Tsuyoshi Nakaza Nanaumi", "apelido": "Nanaumi", "data": "16/02", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/nanaumi_sorrindo.png"},
    {"nome": "João Pedro Kwecko Guimarães", "apelido": "Kwecko", "data": "14/04", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/joao_kwecko_felizinho.png"},
    {"nome": "Guilherme Lubito Dutra", "apelido": "ADM", "data": "06/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/guilherme_lubito_sorrindo.png"},
    {"nome": "Ana Luísa Marzinotti Francisco", "apelido": "Ana Chico", "data": "21/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/ana_chico_sorrindo.png"},
    # Página 2
    {"nome": "Wallace Dametto Teixeira", "apelido": "Wallace", "data": "01/06", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/wallace_sorrindo.png"},
    {"nome": "Felipe Santos Mendonça", "apelido": "Felipe", "data": "19/07", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/felipao_sorrindo.png"},
    {"nome": "Anna Julia Filigoi", "apelido": "Anna", "data": "27/07", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/anna_julia_sorrindo.png"},
    {"nome": "Letícia da Costa Venancio", "apelido": "Letuca", "data": "04/08", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/leticia_sorrindo.png"},
    {"nome": "Mateus Cardoso Santos", "apelido": "Manga", "data": "05/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/mateus_cardoso_feliz.png"},
    {"nome": "Sophia Garcia Sousa", "apelido": "Sophia", "data": "20/11", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/sophia_sorrindo.png"},
    {"nome": "Eduardo Kobata Marto", "apelido": "Kobata", "data": "18/12", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/eduardo_kobata_sorrindo.png"},
    {"nome": "Bruno Soares Alves", "apelido": "Cap", "data": "30/01", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/bruno_sorrindo.png"},
    {"nome": "Helena Prandini Mandl", "apelido": "Helena", "data": "22/03", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/helena_sorrindo.png"},
    {"nome": "Victor Antonio Moraes Pimenta", "apelido": "Pepper", "data": "10/04", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/victor_pimenta_sorrindo.png"},
    {"nome": "Pedro Henrique Pereira Valadão", "apelido": "Baladinha", "data": "12/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/pedro_valadao_sorrindo.png"},
    {"nome": "Gabriel Luiz Patara Buiocchi", "apelido": "Salsicha", "data": "17/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/gabriel_buiocchi_sorrindo.png"},
    {"nome": "Fernanda Matsumoto Lima", "apelido": "Fernandinha", "data": "27/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/fernandinha_sorrindo.png"},
    {"nome": "Pedro de Carvalho Ferreira", "apelido": "Pedro Carvalho", "data": "25/06", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/pedro_carvalho_sorrindo.png"},
    {"nome": "Giovana Dioz Recio", "apelido": "Gi", "data": "07/07", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/gi_sorrindo.png"},
    {"nome": "João Vitor Castelo Branco Diniz", "apelido": "Bolinha", "data": "26/07", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/joao_vitor_diniz_sorrindo.png"},
    {"nome": "Leonardo Ferreira", "apelido": "Leleo", "data": "04/08", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/leonardo_ferreira_sorrindo.png"},
    {"nome": "André Mendes de Almeida Lima", "apelido": "Tijolo", "data": "06/08", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/andre_mendes_feliz.png"},
    {"nome": "Luíza Lima Lattuf", "apelido": "Luíza", "data": "03/09", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/luiza_sorrindo.png"},
    {"nome": "Arthur Ryu Miyashiro", "apelido": "Hamadinha", "data": "05/09", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/arthur_ryu_sorrindo.png"},
    # Página 3
    {"nome": "Lucas Rodrigues Hirashima", "apelido": "Hirashima", "data": "02/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/hirashima_sorrindo.png"},
    {"nome": "Alcenor Guimarães Barbosa", "apelido": "Alcenoia", "data": "16/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/alcenor_sorrindo.png"},
    {"nome": "Pedro Viveiros Lopes", "apelido": "Chuchu", "data": "22/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/pedro_lopes_feliz.png"},
    {"nome": "Beatriz Aimi Ramos Umetsu", "apelido": "Babubia", "data": "16/12", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/bia_sorrindo.png"},
    {"nome": "Rafael Levi Siqueira de Andrade", "apelido": "Levi", "data": "31/12", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/rafael_levi_sorrindo.png"},
    {"nome": "Felipe Pigari Gonçalves", "apelido": "Pigari", "data": "01/01", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/pigari_sorrindo.png"},
    {"nome": "Arthur Tsuzuki Morita", "apelido": "Makita", "data": "01/01", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/arthur_morita_sorrindo.png"},
    {"nome": "Leonardo Tetsuo Moura Hamada", "apelido": "Hamada", "data": "08/01", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/leonardo_hamada_sorrindo.png"},
    {"nome": "Gregório Wernke", "apelido": "Gregório", "data": "16/01", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/gregorio_sorrindo.png"},
    {"nome": "Raphael Batarce Momenté", "apelido": "Rapha", "data": "01/03", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/raphael_batarce_felizinho.png"},
    {"nome": "João Gabriel Iuzviak Mantagute", "apelido": "Mantagute", "data": "24/03", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/mantagute_sorrindo.png"},
    {"nome": "Gabriel Farias De Marco", "apelido": "McLovin", "data": "02/04", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/gabriel_de_marco_sorrindo.png"},
    {"nome": "Enrico Turazza Miraldo", "apelido": "Enrico", "data": "04/04", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/enrico_sorrindo.png"},
    {"nome": "Gustavo Pires Ximenes", "apelido": "Ximene", "data": "02/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/gustavo_ximenes_sorrindo.png"},
    {"nome": "Gabriel de Andrade Gomes", "apelido": "Gabriel", "data": "21/05", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/gabriel_sorrindo.png"},
    {"nome": "Augusto Maciel Guedes", "apelido": "Augusto", "data": "18/07", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/augusto_guedes_sorrindo.png"},
    {"nome": "Pedro Takeshi Suzuki", "apelido": "CEO", "data": "25/07", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/pedro_suzuki_sorrindo.png"},
    {"nome": "Lucas Pace Zerbinatti", "apelido": "Pace", "data": "24/09", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/lucas_pace_sorrindo.png"},
    {"nome": "Isabelle Tenorio", "apelido": "Belle", "data": "02/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/isabelle_tenorio_sorrindo.png"},
    {"nome": "Hari Kharlus Arthur Khāna Tolentino", "apelido": "Hari", "data": "19/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/hari_felizinho.png"},
    # Página 4
    {"nome": "Vítor Souza Mendes da Silva", "apelido": "Vitin", "data": "01/11", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/vitor_souza_sorrindo.png"},
    {"nome": "Maria Clara Nunes Luz da Costa", "apelido": "Nunes", "data": "30/12", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/maria_nunes_sorrindo.png"},
    {"nome": "Matheus Andrade Theophilo", "apelido": "Vamp", "data": "10/01", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/matheus_sorrindo.png"},
    {"nome": "Isabely Ruppel", "apelido": "Ruppel", "data": "14/03", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/isabely_ruppel_felizinha.png"},
    {"nome": "Luis Felipe Azzalin Ukon", "apelido": "Zara", "data": "24/03", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/luis_ukon_sorrindo.png"},
    {"nome": "Rafael Francisco Coutinho Neto", "apelido": "Rafael", "data": "06/06", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/rafael_coutinho_sorrindo.png"},
]

# ==============================================================================
# FRASES E INTRODUÇÕES AUTÊNTICAS DO FLICKBOT
# ==============================================================================
INTRODUCOES_DIA = [
    "🤖 Flickbot disse: 🐜 **Bom dia, formiguinhas!** O dia de hoje começa com o aniversário de uma pessoa muito especial em nossa equipe!",
    "🤖 Flickbot disse: 🐜 **Acorda, formigueiro!** São 06h30 da manhã, a Jetson ainda não caiu e hoje o dia começa em festa na oficina!",
    "🤖 Flickbot disse: 🏎️ **Bom dia, formiguinhas da E-Racing!** Larguem as ferramentas por um segundo porque o calendário do FlickBot apitou!",
    "🤖 Flickbot disse: ⚡ **Bora acordar, formiguinhas!** Mais um dia de correria no projeto, mas hoje temos um motivo extra para comemorar!",
    "🤖 Flickbot disse: 🔧 **Bom dia, formigueiro!** Nem só de solda duvidosa e ata de reunião vive esta equipe. Hoje é dia de festa!",
    "🤖 Flickbot disse: 🐜 **Bom dia!** O próximo que falar que fazer aniversário na oficina é plug-and-play vai levar um tapa! Hoje o dia é de festa!",
    "🤖 Flickbot disse: 🍉 **Acorda, formigueiro!** A gente tem quase a mesma porcentagem de água que uma melancia, a diferença é que hoje, além de ansiedade, a gente tem aniversariante!",
    "🤖 Flickbot disse: 🔥 **Bom dia, E-Racing!** Eu surto mas logo me volto, principalmente porque hoje o formigueiro tá em festa! Taca no gepeto os parabéns e vamo que vamo!",
    "🤖 Flickbot disse: 🍕 **Levanta, rapaziada!** Tá tudo dando errado no projeto mas tudo bem, porque hoje tem aniversário e, com sorte, tem pizza!",
    "🤖 Flickbot disse: 🧯 **Bora acordar!** Controle não tem como pegar fogo, mas a velinha do bolo do aniversariante de hoje com certeza vai!",
    "🤖 Flickbot disse: 📦 **Bom dia, formiguinhas!** Passar na E-Racing é como atacado: você entra em 1 divisão, ganha 2, e ainda tem que dar parabéns às 6h30 da manhã!",
    "🤖 Flickbot disse: 🛠️ **Acorda, equipe!** Confesso que aquela solda de ontem ficou uma merda, mas o dia de hoje tá 100% aprovado porque tem gente ficando mais velha!",
    "🤖 Flickbot disse: 💻 **Bom dia!** Codando com a mente, debugando com o coração e pausando tudo agora pra comemorar o aniversário do dia!",
    "🤖 Flickbot disse: 😭 **Levanta, formigueiro!** Quem dormiu igual um bebê, cagado e chorando, já pode acordar pra comer bolachinha porque hoje é dia de festa!",
    "🤖 Flickbot disse: 🥖 **Bom dia!** Eu vou ter que lutar pelo pão mesmo, ou o aniversariante de hoje vai trazer um café da manhã pra rapaziada da oficina?",
    "🤖 Flickbot disse: 🐦 **Acorda, E-Racing!** Fazer a reunião de suspa com os pássaros às 6 da manhã é muito fofo, mas dar parabéns pro aniversariante de hoje é obrigação!",
    "🤖 Flickbot disse: 💼 **Bom dia!** Se a divisão de business tudo produz, a ela tudo pertence... inclusive os parabéns de hoje! Parem as máquinas e bora celebrar!",
    "🤖 Flickbot disse: 🧠 **Bora pro abate!** Nossa, você precisa estudar pra prob? HAHAHAHA! Pelo menos de dar os parabéns pro aniversariante de hoje você não escapa!",
    "🤖 Flickbot disse: 🧱 **Bom dia, formigueiro!** Eu prefiro trabalhar com uma pedra que não se quebra, mas hoje eu abro exceção pra comemorar o aniversário da nossa argila favorita!",
    "🤖 Flickbot disse: ✨ **Atenção!** Deixa eu mandar um recado pra divisão: o aniversariante de hoje é o PROBLEMA da divisão, mas hoje ele tá ILUMINADO! Parabéns!"
]

MENSAGENS_SUSPENSE_SINGULAR = [
    "🤖 Flickbot disse: Quem será que está ficando mais velho(a) hoje e já pode pagar uma pizza pra oficina inteira? 👀",
    "🤖 Flickbot disse: Preparando os arquivos confidenciais do Gerador de Atas... Achamos o(a) aniversariante do dia! 🥁",
    "🤖 Flickbot disse: Diz a lenda que quem faz aniversário hoje ganha isenção de limpar a oficina (mentira, não ganha não, mas ganha parabéns)! 🎉",
    "🤖 Flickbot disse: Tem gente querendo parabéns e não tá sabendo pedir! Quem será o dono do dia hoje? 👀",
    "🤖 Flickbot disse: Na minha cabeça faz sentido fazer suspense, mas vamos ter que revelar! Quem tá de aniversário? 🥁",
    "🤖 Flickbot disse: Procurando no banco de dados quem é que vai fanar hoje porque o plano de estudos deu errado... Achamos o aniversariante! 🕵️‍♂️",
    "🤖 Flickbot disse: Se fosse pra só falar quem é direto eu contratava um papagaio, mas o FlickBot gosta de suspense! Rufem os tambores... 🦜🥁",
    "🤖 Flickbot disse: Quem diria que o fabricante estava certo! Hoje a garantia de mais um membro da equipe foi renovada. De quem estamos falando? ⚙️",
    "🤖 Flickbot disse: Vamo querê! Vamo virar aniversariante! Quem será que tá subindo de nível hoje na E-Racing? 🏎️👀",
    "🤖 Flickbot disse: Se funciona? Deveria! O sistema do FlickBot apitou que tem alguém envelhecendo no meio do formigueiro... 🚨",
    "🤖 Flickbot disse: Lendo os arquivos de log de DevOps... ERRRRRRRR! Brincadeira, o script rodou liso e achamos o aniversariante! 💻🥁",
    "🤖 Flickbot disse: O homem nasce bom, mas o projeto o corrompe. Quem será que tá completando mais um ano de corrupção automotiva hoje? 🏁👀",
    "🤖 Flickbot disse: Qual a DDP do ar? Não sei, mas a energia hoje tá alta pra revelar quem tá fazendo aniversário! ⚡"
]

MENSAGENS_SUSPENSE_PLURAL = [
    "🤖 Flickbot disse: E hoje não é aniversário em dose única não! Passar na E-Racing é igual atacado: você olha o calendário de hoje e leva aniversariante em dobro! 👀🎉",
    "🤖 Flickbot disse: O formigueiro hoje está em festa múltipla! Segura a sequência de aniversariantes do dia! 🥁🔥",
    "🤖 Flickbot disse: Se um aniversário já dá trabalho, imagina vários! Quem diria que os fabricantes estavam certos e lançaram essa galera toda no mesmo dia? ⚙️👀",
    "🤖 Flickbot disse: Atenção formigueiro! Hoje a gente não tem só um problema, temos vários aniversariantes ILUMINADOS ao mesmo tempo! 🎉",
    "🤖 Flickbot disse: Pra quem não sabe nada, metade é o dobro! E hoje os aniversários vieram dobrados (ou até triplicados)! Rufem os tambores... 🥁",
    "🤖 Flickbot disse: Taca no gepeto que resolve quem é que tá ficando mais velho hoje! Spoiler: é mais de uma pessoa querendo parabéns! 🤖🎂",
    "🤖 Flickbot disse: Hoje o FlickBot tá em chamas! 🔥 Não é um shotinho de parabéns, é um shotão múltiplo no formigueiro! Vem ver quem são os donos do dia!",
    "🤖 Flickbot disse: Se funciona em dose dupla? Deveria! O sistema apitou e temos uma sequência de aniversariantes prontos pro abate hoje! 🚨",
    "🤖 Flickbot disse: A gente não precisa ter tudo, mas os parabéns que tivermos hoje têm que ser os melhores para essa galera toda que faz aniversário junto! 🥳",
    "🤖 Flickbot disse: Até lá, se tiver que dobrar um main hoop num poste pra dar parabéns pra todo mundo de uma vez, a gente vai dobrar! Segura essa lista! 🏎️"
]

# Frases próprias do FlickBot inspiradas diretamente nas pérolas da equipe
FRASES_FLICKBOT_OFICINA = [
    '"Confesso que essa solda ficou duvidosa, mas o seu aniversário ficou 10/10! Parabéns, {apelido}!" — FlickBot, 2026',
    '"Não sou o Lucas, mas estou no meio do formigueiro só pra te dar parabéns, {apelido}!" — FlickBot',
    '"A gente tem quase a mesma porcentagem de água que uma melancia. O que muda é que hoje o(a) {apelido} tem bolo e ansiedade!" — FlickBot',
    '"Se tudo der errado na oficina hoje, é porque era pra dar... menos o aniversário do(a) {apelido}! Comemora!" — FlickBot',
    '"O próximo que falar que o aniversário do(a) {apelido} é plug-and-play vai levar um tapa! Hoje o dia é todo seu!" — FlickBot',
    '"Tá tudo dando errado mas tudo bem, hoje tem aniversário do(a) {apelido} (e esperamos que tenha pizza)!" — FlickBot',
    '"Codar com a mente, debugar com o coração e comemorar o aniversário do(a) {apelido} na oficina sem moderação!" — FlickBot',
    '"Até lá, se tiver que dobrar um main hoop num poste pra comemorar o aniversário do(a) {apelido}, a gente vai dobrar!" — FlickBot',
    '"A gente não precisa ter tudo na oficina, mas o parabéns do(a) {apelido} tem que ser o melhor!" — FlickBot',
    '"Quem diria que o fabricante estava certo quando lançou o(a) {apelido} no mundo! Mais um ano de garantia renovado!" — FlickBot',
    '"Não tem como fazer engenharia e esquecer o aniversário do(a) {apelido}! Parabéns, lenda!" — FlickBot',
    '"Aura não se explica, se sente — e hoje a aura do formigueiro tá todinha no aniversário do(a) {apelido}!" — FlickBot',
    '"Na de você não querer se meter, você já fez mais um ano de vida na E-Racing! Parabéns, {apelido}!" — FlickBot',
    '"Eu surto mas logo me volto, ainda mais pra dar feliz aniversário pro(a) {apelido} às 6h30 da manhã!" — FlickBot',
    '"Tem gente que quer bolo e não tá sabendo pedir! Feliz aniversário, {apelido}!" — FlickBot',
    '"Se ontem você dormiu igual um bebê, cagado e chorando, hoje é dia de acordar pra comemorar! Parabéns, {apelido}!" — FlickBot',
    '"Se a divisão de business tudo produz, o aniversário de hoje a ela tudo pertence! Parabéns, {apelido}!" — FlickBot',
    '"Pra quem não sabe nada, metade é o dobro, mas a sua idade hoje é inteira! Feliz aniversário, {apelido}!" — FlickBot',
    '"Seu sobrenome pode ser perigo, mas hoje o perigo é ficar sem bolo na oficina! Parabéns, {apelido}!" — FlickBot',
    '"Eita como envelhece! Digo... eita como trabalha! Feliz aniversário, {apelido}, aproveita o seu dia!" — FlickBot',
    '"A frase que DevOps carrega é ERRRRRRRR, mas o seu aniversário rodou liso e sem bugs hoje! Parabéns, {apelido}!" — FlickBot',
    '"Todo mecânico médio precisa de uma loirinha de aero, mas hoje você só precisa de parabéns! Feliz aniversário, {apelido}!" — FlickBot',
    '"Seu plano de estudos deu errado e seu plano agora é fanar? Pelo menos hoje tem o seu aniversário pra salvar o dia! Parabéns, {apelido}!" — FlickBot',
    '"O homem nasce bom, mas o projeto o corrompe... Sorte que hoje é seu aniversário pra dar uma purificada! Parabéns, {apelido}!" — FlickBot',
    '"Sem você a equipe ficaria imbotável! Muito sucesso e feliz aniversário, {apelido}!" — FlickBot',
    '"Se fosse pra só dar parabéns eu contratava um papagaio, mas o FlickBot faz questão! Feliz aniversário, {apelido}!" — FlickBot',
    '"Lanterna no lixão não é estrela, mas hoje você é a estrela do formigueiro! Parabéns, {apelido}!" — FlickBot',
    '"Seja Sigma de Eletrônica, Alpha de Powertrain ou Beta de Controle, hoje todo mundo é fã do(a) {apelido}! Parabéns!" — FlickBot',
    '"A Jetson pode até cair, mas o seu pique pro aniversário de hoje não cai nunca! Feliz vida, {apelido}!" — FlickBot',
    '"Precisa de siso pra fazer chassi? Não sei, mas precisa de fôlego pra assoprar a velinha hoje! Parabéns, {apelido}!" — FlickBot',
    '"Se você entrou na academia pra ser menos cabeçudo, hoje pode meter o pé na jaca sem culpa porque é seu dia! Parabéns, {apelido}!" — FlickBot',
    '"Vou acender um incenso na oficina pra limpar as energias e atrair muita sorte pro seu novo ano de vida! Parabéns, {apelido}!" — FlickBot',
    '"Você diz que veio pro abate, mas hoje o único abate vai ser o do seu bolo de aniversário! Parabéns, {apelido}!" — FlickBot',
    '"Não tem cabelo, logo não tem opinião? Brincadeira, hoje a única opinião que importa é a sua! Feliz aniversário, {apelido}!" — FlickBot',
    '"Pelo preço certo o FlickBot faz qualquer coisa, mas te dar feliz aniversário é 100% de graça! Parabéns, {apelido}!" — FlickBot',
    '"Qual a diferença da oficina pra Costa Amalfitana hoje? Nenhuma, o glamour é o mesmo no aniversário do(a) {apelido}! Parabéns!" — FlickBot',
    '"De carona te deixaram só na matéria e ficou sem pai nem parente... Mas no seu aniversário a equipe toda tá aqui, {apelido}!" — FlickBot',
    '"Vamo querê! Vamo virar membro e vamo comer bolo! Parabéns por mais um ano de vida, {apelido}!" — FlickBot'
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
        },
        # ==============================================================================
        # NOVA ADIÇÃO: Assinatura do Flickboss com LinkedIn
        # ==============================================================================
        {
            "type": "TextBlock",
            "text": "Um dos meus principais criadores, [Flickboss](https://www.linkedin.com/in/gideone-carvalho-dos-santos-68479025b/) te deseja parabéns e felicidades sempre! 🚀",
            "wrap": True,
            "size": "Small",
            "isSubtle": True,
            "spacing": "Medium"
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
