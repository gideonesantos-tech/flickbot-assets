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
    {"nome": "Felipe Petrillo Fici Zackiewicz", "apelido": "Fici", "data": "29/10", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/fici%20sorrindo.jpg?raw=true"},
    {"nome": "Cairê Belo da Silva", "apelido": "Cairê", "data": "10/11", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Caire%20sorrindo.png?raw=true"},
    {"nome": "Igor Dela Costa de Oliveira", "apelido": "Igor", "data": "27/12", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/igor%20sorrindo.png?raw=true"},
    {"nome": "Guilherme Souza", "apelido": "Mogli", "data": "02/02", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Guilherme%20sorrindo.png?raw=true"},
    {"nome": "Pedro Jaluul Cardo", "apelido": "Jalulu", "data": "01/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/jaluul%20sorrindo.png?raw=true"},
    {"nome": "Pedro Campanha Neto", "apelido": "Pedro Campanha", "data": "23/12", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Pedro%20Campanha%20sorrindo.png?raw=true"},
    {"nome": "Paulo Rodrigues de Oliveira Nilo", "apelido": "Paulo Rodrigues", "data": "03/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Paulo%20sorrindo.png?raw=true"},
    {"nome": "Maria Clara de Araújo Bianchi", "apelido": "Maria", "data": "17/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Maria%20Bianchi%20sorrindo.png?raw=true"},
    {"nome": "Davi Roldão Siqueira", "apelido": "Davi", "data": "05/06", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Davi%20sorrindo.png?raw=true"},
    {"nome": "Ana Beatriz Alves Chammas", "apelido": "Chammas", "data": "13/10", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Ana%20Chammas%20sorrindo.png?raw=true"},
    {"nome": "Daniel Abraão de Brito Nogueira", "apelido": "Daniel", "data": "23/10", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Daniel%20sorrindo.png?raw=true"},
    {"nome": "Artur Dias de Oliveira", "apelido": "Artur", "data": "27/11", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Artur%20Oliveira%20sorrindo.png?raw=true"},
    {"nome": "Jéssica Ramos dos Santos", "apelido": "Jéssica", "data": "13/12", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/J%C3%A9ssica%20sorrindo.png?raw=true"},
    {"nome": "Paulo Vitor Figueiredo da Silva", "apelido": "Paulo Vitor", "data": "20/12", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Paulo%20vitor%20sorrindo.png?raw=true"},
    {"nome": "Mateus Silva Cirino", "apelido": "Teteu", "data": "14/01", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Mateus%20Cirino%20sorrindo.png?raw=true"},
    {"nome": "Rodolfo Yoon Sang Joo", "apelido": "Rodolfera", "data": "03/02", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/rodolfo%20sorrindo.png?raw=true"},
    {"nome": "Arthur Tsuyoshi Nakaza Nanaumi", "apelido": "Nanaumi", "data": "16/02", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Nanaumi%20sorrindo.png?raw=true"},
    {"nome": "João Pedro Kwecko Guimarães", "apelido": "Kwecko", "data": "14/04", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Jo%C3%A3o%20Kwecko%20felizinho.png?raw=true"},
    {"nome": "Guilherme Lubito Dutra", "apelido": "ADM", "data": "06/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Guilherme%20Lubito%20sorrindo.png?raw=true"},
    {"nome": "Ana Luísa Marzinotti Francisco", "apelido": "Ana Chico", "data": "21/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/ana%20chico%20sorrindo.png?raw=true"},
    # Página 2
    {"nome": "Wallace Dametto Teixeira", "apelido": "Wallace", "data": "01/06", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/wallace%20sorrindo.png?raw=true"},
    {"nome": "Felipe Santos Mendonça", "apelido": "Felipe", "data": "19/07", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/felip%C3%A3o%20sorrindo.png?raw=true"},
    {"nome": "Anna Julia Filigoi", "apelido": "Anna", "data": "27/07", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/anna%20julia%20sorrindo.png?raw=true"},
    {"nome": "Letícia da Costa Venancio", "apelido": "Letuca", "data": "04/08", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/leticia%20sorrindo.png?raw=true"},
    {"nome": "Mateus Cardoso Santos", "apelido": "Manga", "data": "05/10", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Mateus%20Cardoso%20(manga)%20feliz.png?raw=true"},
    {"nome": "Sophia Garcia Sousa", "apelido": "Sophia", "data": "20/11", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Sophia%20sorrindo.png?raw=true"},
    {"nome": "Eduardo Kobata Marto", "apelido": "Kobata", "data": "18/12", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Eduardo%20Kobata%20sorrindo.png?raw=true"},
    {"nome": "Bruno Soares Alves", "apelido": "Cap", "data": "30/01", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/bruno%20sorrindo.png?raw=true"},
    {"nome": "Helena Prandini Mandl", "apelido": "Helena", "data": "22/03", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Helena%20sorrindo.png?raw=true"},
    {"nome": "Victor Antonio Moraes Pimenta", "apelido": "Pepper", "data": "10/04", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Victor%20Pimenta%20(little%20pepper)%20sorrindo.png?raw=true"},
    {"nome": "Pedro Henrique Pereira Valadão", "apelido": "Baladinha", "data": "12/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Pedro%20Valad%C3%A3o%20sorrindo.png?raw=true"},
    {"nome": "Gabriel Luiz Patara Buiocchi", "apelido": "Salsicha", "data": "17/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Gabriel%20Buiocchi%20(Sausage)%20sorrindo.png?raw=true"},
    {"nome": "Fernanda Matsumoto Lima", "apelido": "Fernandinha", "data": "27/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Fernandinha%20sorrindo.png?raw=true"},
    {"nome": "Pedro de Carvalho Ferreira", "apelido": "Pedro Carvalho", "data": "25/06", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/pedro%20carvalho%20sorrindo.png?raw=true"},
    {"nome": "Giovana Dioz Recio", "apelido": "Gi", "data": "07/07", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/gi%20sorrindo.png?raw=true"},
    {"nome": "João Vitor Castelo Branco Diniz", "apelido": "Bolinha", "data": "26/07", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Jo%C3%A3o%20Vitor%20Diniz%20(bolinha)%20sorrindo%20feliz.png?raw=true"},
    {"nome": "Leonardo Ferreira", "apelido": "Leleo", "data": "04/08", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Leonardo%20Ferreira%20sorrindo.png?raw=true"},
    {"nome": "André Mendes de Almeida Lima", "apelido": "Tijolo", "data": "06/08", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Andr%C3%A9%20Mendes%20(tijolo)%20feliz.png?raw=true"},
    {"nome": "Luíza Lima Lattuf", "apelido": "Luíza", "data": "03/09", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/main/fotos/Luiza%20sorrindo.png"},
    {"nome": "Arthur Ryu Miyashiro", "apelido": "Hamadinha", "data": "05/09", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Arthur%20Ryu%20sorrindo%20felizinho.png?raw=true"},
    # Página 3
    {"nome": "Lucas Rodrigues Hirashima", "apelido": "Hirashima", "data": "02/10", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/hirashima%20sorrindo.png?raw=true"},
    {"nome": "Alcenor Guimarães Barbosa", "apelido": "Alcenoia", "data": "16/10", "foto": "https://raw.githubusercontent.com/gideonesantos-tech/flickbot-assets/refs/heads/main/fotos/Alcenor%20sorrindo.png"},
    {"nome": "Pedro Viveiros Lopes", "apelido": "Chuchu", "data": "22/10", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Pedro%20Lopes%20(chuchu)%20feliz.png?raw=true"},
    {"nome": "Beatriz Aimi Ramos Umetsu", "apelido": "Babubia", "data": "16/12", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/bia%20sorrindo.png?raw=true"},
    {"nome": "Rafael Levi Siqueira de Andrade", "apelido": "Levi", "data": "31/12", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Rafael%20Levi%20sorrindo.png?raw=true"},
    {"nome": "Felipe Pigari Gonçalves", "apelido": "Pigari", "data": "01/01", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/pigari%20sorrindo.png?raw=true"},
    {"nome": "Arthur Tsuzuki Morita", "apelido": "Makita", "data": "01/01", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Arthur%20Morita%20sorrindo.png?raw=true"},
    {"nome": "Leonardo Tetsuo Moura Hamada", "apelido": "Hamada", "data": "08/01", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Leonardo%20Hamada%20sorrindo.png?raw=true"},
    {"nome": "Gregório Wernke", "apelido": "Gregório", "data": "16/01", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Greg%C3%B3rio%20sorrindo.png?raw=true"},
    {"nome": "Raphael Batarce Momenté", "apelido": "Rapha", "data": "01/03", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Raphael%20Batarce%20felizinho.png?raw=true"},
    {"nome": "João Gabriel Iuzviak Mantagute", "apelido": "Mantagute", "data": "24/03", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/mantagute%20sorrindo.png?raw=true"},
    {"nome": "Gabriel Farias De Marco", "apelido": "McLovin", "data": "02/04", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Gabriel%20De%20Marco%20sorrindo.png?raw=true"},
    {"nome": "Enrico Turazza Miraldo", "apelido": "Enrico", "data": "04/04", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Enrico%20sorrindo.png?raw=true"},
    {"nome": "Gustavo Pires Ximenes", "apelido": "Ximene", "data": "02/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Gustavo%20Ximenes%20sorrindo.png?raw=true"},
    {"nome": "Gabriel de Andrade Gomes", "apelido": "Gabriel", "data": "21/05", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Gabriel%20sorrindo.png?raw=true"},
    {"nome": "Augusto Maciel Guedes", "apelido": "Augusto", "data": "18/07", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Augusto%20Guedes%20sorrindo.png?raw=true"},
    {"nome": "Pedro Takeshi Suzuki", "apelido": "CEO", "data": "25/07", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Pedro%20Suzuki%20sorrindo.png?raw=true"},
    {"nome": "Lucas Pace Zerbinatti", "apelido": "Pace (leia como quiser)", "data": "24/09", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Lucas%20Pace%20sorrindo.png?raw=true"},
    {"nome": "Isabelle Tenorio", "apelido": "Belle", "data": "02/10", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Isabelle%20Tenorio%20sorrindo.png?raw=true"},
    {"nome": "Hari Kharlus Arthur Khāna Tolentino", "apelido": "Hari", "data": "19/10", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/hari%20felizinho.png?raw=true"},
    # Página 4
    {"nome": "Vítor Souza Mendes da Silva", "apelido": "Vitin", "data": "01/11", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/V%C3%ADtor%20Souza%20sorrindo.png?raw=true"},
    {"nome": "Maria Clara Nunes Luz da Costa", "apelido": "Nunes", "data": "30/12", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Maria%20Nunes%20sorrindo.png?raw=true"},
    {"nome": "Matheus Andrade Theophilo", "apelido": "Vamp", "data": "10/01", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Matheus%20sorrindo.png?raw=true"},
    {"nome": "Isabely Ruppel", "apelido": "Ruppel", "data": "14/03", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Isabely%20Ruppel%20felizinha.png?raw=true"},
    {"nome": "Luis Felipe Azzalin Ukon", "apelido": "Zara", "data": "24/03", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Luis%20Ukon%20(Zara)%20sorrindo.png?raw=true"},
    {"nome": "Rafael Francisco Coutinho Neto", "apelido": "Rafael", "data": "06/06", "foto": "https://github.com/gideonesantos-tech/flickbot-assets/blob/main/fotos/Rafael%20Coutinho%20sorrindo.png?raw=true"},
]

# ==============================================================================
# FRASES E INTRODUÇÕES AUTÊNTICAS DO FLICKBOT
# ==============================================================================
INTRODUCOES_DIA = [
    "🐜 **Bom dia, formiguinhas!** O dia de hoje começa com o aniversário de uma pessoa muito especial em nossa equipe!",
    "🐜 **Acorda, formigueiro!** São 06h30 da manhã, a Jetson ainda não caiu e hoje o dia começa em festa na oficina!",
    "🏎️ **Bom dia, formiguinhas da E-Racing!** Larguem as ferramentas por um segundo porque o calendário do FlickBot apitou!",
    "⚡ **Bora acordar, formiguinhas!** Mais um dia de correria no projeto, mas hoje temos um motivo extra para comemorar!",
    "🔧 **Bom dia, formigueiro!** Nem só de solda duvidosa e ata de reunião vive esta equipe. Hoje é dia de festa!",
    "🐜 **Bom dia!** O próximo que falar que fazer aniversário na oficina é plug-and-play vai levar um tapa! Hoje o dia é de festa!",
    "🍉 **Acorda, formigueiro!** A gente tem quase a mesma porcentagem de água que uma melancia, a diferença é que hoje, além de ansiedade, a gente tem aniversariante!",
    "🔥 **Bom dia, E-Racing!** Eu surto mas logo me volto, principalmente porque hoje o formigueiro tá em festa! Taca no gepeto os parabéns e vamo que vamo!",
    "🍕 **Levanta, rapaziada!** Tá tudo dando errado no projeto mas tudo bem, porque hoje tem aniversário e, com sorte, tem pizza!",
    "🧯 **Bora acordar!** Controle não tem como pegar fogo, mas a velinha do bolo do aniversariante de hoje com certeza vai!",
    "📦 **Bom dia, formiguinhas!** Passar na E-Racing é como atacado: você entra em 1 divisão, ganha 2, e ainda tem que dar parabéns às 6h30 da manhã!",
    "🛠️ **Acorda, equipe!** Confesso que aquela solda de ontem ficou uma merda, mas o dia de hoje tá 100% aprovado porque tem gente ficando mais velha!",
    "💻 **Bom dia!** Codando com a mente, debugando com o coração e pausando tudo agora pra comemorar o aniversário do dia!",
    "😭 **Levanta, formigueiro!** Quem dormiu igual um bebê, cagado e chorando, já pode acordar pra comer bolachinha porque hoje é dia de festa!",
    "🥖 **Bom dia!** Eu vou ter que lutar pelo pão mesmo, ou o aniversariante de hoje vai trazer um café da manhã pra rapaziada da oficina?",
    "🐦 **Acorda, E-Racing!** Fazer a reunião de suspa com os pássaros às 6 da manhã é muito fofo, mas dar parabéns pro aniversariante de hoje é obrigação!",
    "💼 **Bom dia!** Se a divisão de business tudo produz, a ela tudo pertence... inclusive os parabéns de hoje! Parem as máquinas e bora celebrar!",
    "🧠 **Bora pro abate!** Nossa, você precisa estudar pra prob? HAHAHAHA! Pelo menos de dar os parabéns pro aniversariante de hoje você não escapa!",
    "🧱 **Bom dia, formigueiro!** Eu prefiro trabalhar com uma pedra que não se quebra, mas hoje eu abro exceção pra comemorar o aniversário da nossa argila favorita!",
    "✨ **Atenção!** Deixa eu mandar um recado pra divisão: o aniversariante de hoje é o PROBLEMA da divisão, mas hoje ele tá ILUMINADO! Parabéns!"
]

MENSAGENS_SUSPENSE_SINGULAR = [
    "Quem será que está ficando mais velho(a) hoje e já pode pagar uma pizza pra oficina inteira? 👀",
    "Preparando os arquivos confidenciais do Gerador de Atas... Achamos o(a) aniversariante do dia! 🥁",
    "Diz a lenda que quem faz aniversário hoje ganha isenção de limpar a oficina (mentira, não ganha não, mas ganha parabéns)! 🎉",
    "Tem gente querendo parabéns e não tá sabendo pedir! Quem será o dono do dia hoje? 👀",
    "Na minha cabeça faz sentido fazer suspense, mas vamos ter que revelar! Quem tá de aniversário? 🥁",
    "Procurando no banco de dados quem é que vai fanar hoje porque o plano de estudos deu errado... Achamos o aniversariante! 🕵️‍♂️",
    "Se fosse pra só falar quem é direto eu contratava um papagaio, mas o FlickBot gosta de suspense! Rufem os tambores... 🦜🥁",
    "Quem diria que o fabricante estava certo! Hoje a garantia de mais um membro da equipe foi renovada. De quem estamos falando? ⚙️",
    "Vamo querê! Vamo virar aniversariante! Quem será que tá subindo de nível hoje na E-Racing? 🏎️👀",
    "Se funciona? Deveria! O sistema do FlickBot apitou que tem alguém envelhecendo no meio do formigueiro... 🚨",
    "Lendo os arquivos de log de DevOps... ERRRRRRRR! Brincadeira, o script rodou liso e achamos o aniversariante! 💻🥁",
    "O homem nasce bom, mas o projeto o corrompe. Quem será que tá completando mais um ano de corrupção automotiva hoje? 🏁👀",
    "Qual a DDP do ar? Não sei, mas a energia hoje tá alta pra revelar quem tá fazendo aniversário! ⚡"
]

MENSAGENS_SUSPENSE_PLURAL = [
    "E hoje não é aniversário em dose única não! Passar na E-Racing é igual atacado: você olha o calendário de hoje e leva aniversariante em dobro! 👀🎉",
    "O formigueiro hoje está em festa múltipla! Segura a sequência de aniversariantes do dia! 🥁🔥",
    "Se um aniversário já dá trabalho, imagina vários! Quem diria que os fabricantes estavam certos e lançaram essa galera toda no mesmo dia? ⚙️👀",
    "Atenção formigueiro! Hoje a gente não tem só um problema, temos vários aniversariantes ILUMINADOS ao mesmo tempo! 🎉",
    "Pra quem não sabe nada, metade é o dobro! E hoje os aniversários vieram dobrados (ou até triplicados)! Rufem os tambores... 🥁",
    "Taca no gepeto que resolve quem é que tá ficando mais velho hoje! Spoiler: é mais de uma pessoa querendo parabéns! 🤖🎂",
    "Hoje o FlickBot tá em chamas! 🔥 Não é um shotinho de parabéns, é um shotão múltiplo no formigueiro! Vem ver quem são os donos do dia!",
    "Se funciona em dose dupla? Deveria! O sistema apitou e temos uma sequência de aniversariantes prontos pro abate hoje! 🚨",
    "A gente não precisa ter tudo, mas os parabéns que tivermos hoje têm que ser os melhores para essa galera toda que faz aniversário junto! 🥳",
    "Até lá, se tiver que dobrar um main hoop num poste pra dar parabéns pra todo mundo de uma vez, a gente vai dobrar! Segura essa lista! 🏎️"
]

# Frases próprias do FlickBot inspiradas diretamente nas pérolas das Atas da oficina
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
                            "facts": [
                                {"title": "Apelido na Oficina:", "value": membro["apelido"]},
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
