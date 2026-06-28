# ===========================================
# 1 - Importando as bibliotecas necessárias
# ===========================================
import json, random, os
from datetime import datetime, timedelta

# ===========================================
# 2 - Criando uma pasta para execucao em qualquer ambiente
# ===========================================
PASTA_BRONZE_FONTES_EXTERNAS = "data_lakehouse/bronze"
os.makedirs(PASTA_BRONZE_FONTES_EXTERNAS, exist_ok = True)

# =========================================================
# 3 - Funcao para gerar datas de forma aleatoria
# =========================================================
def gerarData():
    data_inicio = datetime(2026, 1, 1)
    dia = random.randint(1, 150)

    # Dependendo do retorno da funcao random, a variavel hora, recebera um valor, pensando num cenario de pico ou entrepico na carga 
    if random.random() < 0.70:
        hora = random.choice([0, 1, 2, 3, 4, 10, 11, 12, 13])
    else:
        hora = random.choice([5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
      
    minuto = random.randint(1, 59)
    segundo = random.randint(0, 59)
    data_escolhida = data_inicio + timedelta(days = dia, hours = hora, minutes = minuto, seconds = segundo)
    return data_escolhida

# ==================================================================================
# 4 - Estruturas de Dados usadas para simular o que foi coletado de APIs / Scraping
# ==================================================================================
baseNoticias = [
    # POSITIVAS
    "Lumina Energy anuncia expansão de 50 novos eletropostos rápidos em Porto Real.",
    "Parceria entre Prefeitura e Lumina Energy zera tarifa de recarga para ônibus elétricos escolares.",
    "Porto Real bate recorde nacional e atinge 70% da frota pública movida a energia limpa.",
    "Investidores internacionais injetam R$ 45 milhões na rede de eletropostos da Lumina.",
    "Nova tecnologia da Lumina reduz tempo de carregamento de ônibus elétricos para apenas 20 minutos.",
    "Lumina Energy recebe prêmio ambiental de inovação tecnológica em mobilidade urbana.",
    # NEGATIVAS
    "Tarifa de energia em Porto Real deve sofrer reajuste severo de 12% no próximo mês.",
    "Apagão parcial atinge o Distrito Industrial de Porto Real e paralisa frota de ônibus elétricos.",
    "Eletroposto no Jardim Oceânico apresenta falha crônica na tensão e queima bateria de veículo público.",
    "Moradores protestam na Estação Central contra o aumento abusivo nas taxas de recarga da Lumina.",
    "Falha no sistema de faturamento da Lumina Energy gera cobranças duplicadas e aciona o Procon.",
    "Onda de calor extremo sobrecarrega subestação e desliga eletropostos na Vila Elétrica por segurança."
]

baseRedeSociais = [
    # POSITIVAS
    "Parabéns @LuminaEnergy! O novo eletroposto do Centro Histórico ficou show! Carregou meu ônibus voando! ⚡",
    "Muito bom ver Porto Real virando referência em sustentabilidade. Os novos carregadores rápidos salvam o dia! 🙌",
    "Aplicativo da Lumina atualizou e agora dá para reservar a vaga de recarga antes de chegar. Sensacional!",
    "Motorista de aplicativo aqui. Com esses novos postos de 750V no Portal do Vale, meu lucro aumentou muito. Valeu!",
    "Finalmente eletropostos de verdade no Bairro das Nações! Tudo limpo, rápido e funcionando perfeitamente.",
    "Adorei o atendimento do suporte da @LuminaEnergy na estação Novo Horizonte. Resolveram meu problema na hora! 👍",
    # NEGATIVAS 
    "Um absurdo a falta de energia nos carregadores do Parque Tecnológico hoje cedo. Que serviço péssimo! 😡",
    "Alguém mais notou que o aplicativo de faturamento da Lumina está cobrando valores errados nas últimas recargas?",
    "Fiquei preso no eletroposto da Estação Central porque a tensão caiu para zero do nada. Que decepção total.",
    "A tarifa de recarga da @LuminaEnergy está ficando mais cara do que rodar a diesel... Desse jeito quebram o trabalhador!",
    "Mais uma vez fila imensa no eletroposto de Porto Novo porque metade dos carregadores está quebrada de novo. Vergonha.",
    "Minha recarga foi interrompida três vezes sozinhas na Vila Elétrica. O app travou e continuou descontando meu saldo! 🤬"
]

baseScraping = [
    # POSITIVAS 
    "O debate sobre a infraestrutura de recarga em Porto Real ganha força positiva. Especialistas apontam que a nova rede de alta tensão implementada pela Lumina mitigou os antigos problemas de oscilação, garantindo um carregamento linear e extremamente seguro para as frotas pesadas.",
    "Análise profunda do mercado energético mostra que a Lumina Energy domina o setor em Porto Real com inovação. O grande acerto técnico foi a integração do protocolo OCPP com os novos inversores da WEG, resultando em uma eficiência energética sem precedentes no país.",
    "Um review técnico detalhado publicado no portal Eletromobilidade Real elogiou a estabilidade dos novos carregadores de 750V instalados no Jardim Oceânico. O autor ressalta que, apesar do investimento inicial, o custo-benefício para frotas comerciais é imbatível a longo prazo.",
    "Entrevistas realizadas no Blog da Comunidade revelam alto índice de satisfação com os novos eletropostos instalados nos bairros periféricos. Motoristas de vans municipais relatam que a transição para a matriz elétrica reduziu os custos operacionais de transporte em até quarenta por cento.",
    "Especialistas em urbanismo destacam no fórum Mobilidade do Amanhã que a infraestrutura planejada pela Lumina Energy ajudou a reduzir drasticamente os índices de poluição sonora e atmosférica nas grandes avenidas do Centro Histórico durante os horários de pico.",
    "O Portal Energia do Futuro publicou um artigo celebrando o sucesso da operação dos eletropostos rápidos na rodovia de Porto Real. A facilidade de pagamento integrada via carteiras digitais e Pix reduziu o tempo de parada dos veículos de entrega interestaduais.",
    # NEGATIVAS
    "Gargalos estruturais graves continuam gerando dor de cabeça. Usuários de um conhecido fórum automotivo local alertam que a recorrente queda de tensão registrada nos sensores dos postes aponta para o subdimensionamento crônico da rede elétrica controlada pela concessionária regional.",
    "Moradores de bairros populosos de Porto Real organizaram um abaixo-assinado virtual cobrando transparência da Lumina Energy. Segundo postagens inflamadas no Blog da Comunidade, o faturamento confuso e as taxas flutuantes inviabilizam o planejamento financeiro dos motoristas autônomos.",
    "Relatório técnico independente acende um sinal vermelho para a segurança dos eletropostos na Cidade Alta. Amostras coletadas indicam que picos severos de corrente elétrica ocorrem quando múltiplos ônibus pesados tentam utilizar o sistema simultaneamente, gerando riscos de pane.",
    "A polêmica sobre os reajustes tarifários da Lumina Energy ganhou novos capítulos esta semana. Blogueiros de finanças locais argumentam que os aumentos sucessivos sem uma contrapartida na manutenção dos carregadores quebrados podem frear a adesão à eletrificação na região.",
    "Postagens rastreadas no Fórum Energia Real criticam duramente o descaso com os pontos de recarga do Distrito Industrial. Relatos apontam que a falta de cobertura física deixa os equipamentos expostos às intempéries climáticas, acelerando a degradação e causando curto-circuitos.",
    "Usuários relatam no Twitter e em blogs de tecnologia uma vulnerabilidade severa no pareamento do aplicativo da Lumina. Dezenas de motoristas alegam que o sistema não encerra a sessão de cobrança após o cabo ser desconectado, continuando a faturar minutos fantasmas dos clientes."
]

# ================================================================
# 5 - Gerando as estruturas de dados que recebem os dados externos
# ================================================================

def gerarNoticias(quantidade = 40):
    dadosNoticias = []
    for i in range (1, quantidade + 1):
        data = gerarData()
        data_noticia = data.strftime("%Y-%m-%d %H:%M:%S")
        dadosNoticias.append({
            "IDNoticia": f"NOT_{i}",
            "Fonte": random.choice(["Yahoo Finance", "Porto Real News", "Globo Energia", "Diário Sustentável"]),
            "DataPublicacao": data_noticia,
            "Manchete": random.choice(baseNoticias),
            "Autor": random.choice(["Carlos M.", "Juliana S.", "Pedro A.", "Redação"])
        })
    return dadosNoticias

def gerarPostsRedesSociais(quantidade = 60):
    dadosRedes = []
    for i in range(1, quantidade + 1):
        data = gerarData()
        data_redes = data.strftime("%Y-%m-%d %H:%M:%S")
        dadosRedes.append({
            "IDPost": f"POST_{i}",
            "Plataforma": random.choice(["X/Twitter", "LinkedIn", "Instagram"]),
            "DataPostagem": data_redes,
            "Usuario": f"@user_{random.randint(1000, 99999)}",
            "TextoPost": random.choice(baseRedeSociais)
        })
    return dadosRedes

def gerarScraping(quantidade = 40):
    dadosScraping = []
    fontes_scraping = [
        {"nome": "Blog Mobilidade Porto Real", "url": "https://blog.mobilidadeprt.com.br/artigos/"},
        {"nome": "Fórum Energia do Futuro", "url": "https://forum.energiafuturo.com/topico/"},
        {"nome": "Portal Eletromobilidade Real", "url": "https://eletromobilidadereal.com/noticias/"}
    ]
    for i in range(1, quantidade + 1):
        data = gerarData()
        data_scraping = data.strftime("%Y-%m-%d %H:%M:%S")
        fonte_escolhida = random.choice(fontes_scraping)
        dadosScraping.append({
            "IDScraping": f"SCRAP_{i}",
            "SiteOrigem": fonte_escolhida["nome"],
            "UrlColeta": f"{fonte_escolhida['url']}artigo_{random.randint(100, 9999)}.html",
            "DataColeta": data_scraping,
            "HTMLBruto": random.choice(baseScraping)
        })
    return dadosScraping

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("Iniciando a simulacao da ingestao de dados externos (APIs / Web Scraping)")

    # Gerando as estruturas de dados resultantes de cada funcao
    noticias = gerarNoticias(quantidade = 40)
    redesSociais = gerarPostsRedesSociais(quantidade = 60)
    scraping = gerarScraping(quantidade = 40)


    # Definindo os caminhos para salvamento
    caminho_noticias = os.path.join(PASTA_BRONZE_FONTES_EXTERNAS, f"NoticiasBruto.json")
    caminho_redes = os.path.join(PASTA_BRONZE_FONTES_EXTERNAS, f"RedesSociaisBruto.json")
    caminho_scraping = os.path.join(PASTA_BRONZE_FONTES_EXTERNAS, f"ScrapingBruto.json")

    # Salvando os arquivos no formato JSON bruto
    with open(caminho_noticias, "w", encoding = "utf-8") as arquivo:
        json.dump(noticias, arquivo, indent = 4, ensure_ascii = False)

    with open(caminho_redes, "w", encoding = "utf-8") as arquivo:
        json.dump(redesSociais, arquivo, indent = 4, ensure_ascii = False)

    with open(caminho_scraping, "w", encoding = "utf-8") as arquivo:
        json.dump(scraping, arquivo, indent = 4, ensure_ascii = False)

    print("Dados de APIs e Web Scraping salvos com absoluto sucesso na Camada Bronze!")
    print(f"Arquivos JSON gerados com sucesso na pasta: '{PASTA_BRONZE_FONTES_EXTERNAS}'")

