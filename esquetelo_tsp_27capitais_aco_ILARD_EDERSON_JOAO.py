# ==============================================================================
# 🐜 MARCO 2: ESQUELETO DE OTIMIZAÇÃO POR COLÔNIA DE FORMIGAS (ACO / ANT SYSTEM)
# Componente Curricular: Tópicos Avançados em Computação I — IFPA Ananindeua
# Data de Kickoff: 06/11/2026 | Prazo de Entrega: 20/11/2026 (CLASSROOM — 2,5 pts)
# ==============================================================================
#
# PROBLEMA: Caixeiro Viajante das 27 Capitais Brasileiras (26 Capitais + DF)
# ESPAÇO DE BUSCA: (27 - 1)! / 2 ≈ 2,01 × 10²⁶ rotas possíveis.
#
# INSTRUÇÕES PARA A EQUIPE:
# Complete as lacunas marcadas com "🚩 TODO" abaixo para implementar o algoritmo
# Ant Colony Optimization (ACO) de Marco Dorigo e encontrar o circuito de menor
# extensão terrestre/aérea pelo Brasil.
# ==============================================================================

import math
import random
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# 📍 DICIONÁRIO DE DADOS: 27 CAPITAIS BRASILEIRAS (Latitude, Longitude)
# (Já pré-carregado para a equipe)
# ------------------------------------------------------------------------------
CAPITAIS_BRASIL = {
    "Rio Branco (AC)": (-9.975, -67.810),
    "Maceió (AL)": (-9.666, -35.735),
    "Macapá (AP)": (0.035, -51.070),
    "Manaus (AM)": (-3.119, -60.021),
    "Salvador (BA)": (-12.971, -38.510),
    "Fortaleza (CE)": (-3.717, -38.543),
    "Brasília (DF)": (-15.780, -47.930),
    "Vitória (ES)": (-20.315, -40.312),
    "Goiânia (GO)": (-16.686, -49.264),
    "São Luís (MA)": (-2.530, -44.302),
    "Cuiabá (MT)": (-15.601, -56.097),
    "Campo Grande (MS)": (-20.443, -54.647),
    "Belo Horizonte (MG)": (-19.921, -43.938),
    "Belém (PA)": (-1.455, -48.502),
    "João Pessoa (PB)": (-7.115, -34.863),
    "Curitiba (PR)": (-25.428, -49.273),
    "Recife (PE)": (-8.047, -34.877),
    "Teresina (PI)": (-5.089, -42.802),
    "Rio de Janeiro (RJ)": (-22.906, -43.172),
    "Natal (RN)": (-5.795, -35.209),
    "Porto Alegre (RS)": (-30.034, -51.217),
    "Porto Velho (RO)": (-8.761, -63.903),
    "Boa Vista (RR)": (2.823, -60.675),
    "Florianópolis (SC)": (-27.595, -48.548),
    "São Paulo (SP)": (-23.550, -46.633),
    "Aracaju (SE)": (-10.911, -37.071),
    "Palmas (TO)": (-10.184, -48.333)
}

LISTA_CIDADES = list(CAPITAIS_BRASIL.keys())
N_CIDADES = len(LISTA_CIDADES)

def haversine(coord1, coord2):
    """Calcula a distância geodésica em km entre dois pontos geográficos."""
    R = 6371.0 # Raio da Terra em km
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ------------------------------------------------------------------------------
# 🚩 TODO 1: MATRIZ DE DISTÂNCIAS E INVERSO DA DISTÂNCIA (VISIBILIDADE HEURÍSTICA eta)
# ------------------------------------------------------------------------------
matriz_distancias = np.zeros((N_CIDADES, N_CIDADES))
eta = np.zeros((N_CIDADES, N_CIDADES))

# 📌 TODO 1.1: Preencha matriz_distancias usando a função haversine(c1, c2)
# 📌 TODO 1.2: Preencha a matriz de visibilidade eta[i][j] = 1.0 / matriz_distancias[i][j] (para i != j)
for i in range(N_CIDADES):
    for j in range(N_CIDADES):
        if i != j:
            # === DESENVOLVA AQUI ===
            dist = haversine(CAPITAIS_BRASIL[LISTA_CIDADES[i]], CAPITAIS_BRASIL[LISTA_CIDADES[j]])
            matriz_distancias[i][j] = dist
            eta[i][j] = 1.0 / dist

print("✅ Matrizes de distância e visibilidade heurística (eta) inicializadas.")

# ------------------------------------------------------------------------------
# ⚙️ HIPERPARÂMETROS DO ALGORITMO ACO
# ------------------------------------------------------------------------------
ALPHA = 1.0       # Peso da intensidade de feromônio (tau)
BETA = 3.0        # Peso da visibilidade heurística (eta = 1/d)
RHO = 0.1         # Taxa de evaporação do feromônio (0.1 = 10% por iteração)
Q = 100.0         # Constante de depósito de feromônio
N_FORMIGAS = 30   # Número de formigas artificiais por iteração
N_ITERACOES = 150 # Número total de iterações do enxame

# Inicialização da Matriz de Feromônio tau com valor inicial pequeno (ex: 0.1)
tau = np.ones((N_CIDADES, N_CIDADES)) * 0.1

# ------------------------------------------------------------------------------
# 🚩 TODO 2: REGRA DE TRANSIÇÃO PROBABILÍSTICA (Seleção da Próxima Cidade)
# ------------------------------------------------------------------------------
def escolher_proxima_cidade(cidade_atual, nao_visitadas, tau, eta, alpha, beta):
    """
    Calcula a probabilidade de transição p_{ij} para cada cidade j em nao_visitadas:
    p_{ij} = (tau[i][j]^alpha * eta[i][j]^beta) / sum(tau[i][k]^alpha * eta[i][k]^beta)

    Retorna o índice da próxima cidade selecionada probabilisticamente.
    """
    probabilidades = []

    # 📌 TODO 2.1: Calcule o fator p = (tau[atual][proxima]**alpha) * (eta[atual][proxima]**beta)
    # para cada cidade em nao_visitadas e adicione à lista 'probabilidades'

    # === DESENVOLVA AQUI ===
    for proxima in nao_visitadas:
        p = (tau[cidade_atual][proxima] ** alpha) * (eta[cidade_atual][proxima] ** beta)
        probabilidades.append(p)

    # Normalização das probabilidades para soma = 1.0
    soma_prob = sum(probabilidades)
    if soma_prob == 0 or math.isnan(soma_prob):
        return random.choice(nao_visitadas)

    probabilidades_norm = [p / soma_prob for p in probabilidades]

    # Seleção estocástica com base nas probabilidades calculadas
    cidade_escolhida = np.random.choice(nao_visitadas, p=probabilidades_norm)
    return cidade_escolhida

# ------------------------------------------------------------------------------
# 🚩 TODO 3: FUNÇÃO DE AVALIAÇÃO DA ROTA (COMPRIMENTO DO CIRCUITO FECHADO)
# ------------------------------------------------------------------------------
def calcular_distancia_rota(rota):
    """
    Recebe uma lista com a sequência das cidades (ex: [0, 14, 5, ..., 21]).
    Retorna a distância total em km incluindo o retorno à cidade inicial.
    """
    distancia = 0.0
    # 📌 TODO 3.1: Some as distâncias dos trechos consecutivos na matriz_distancias
    # DICA: c1 = rota[i], c2 = rota[(i + 1) % len(rota)]

    # === DESENVOLVA AQUI ===
    for i in range(len(rota)):
        c1 = rota[i]
        c2 = rota[(i + 1) % len(rota)]
        distancia += matriz_distancias[c1][c2]

    return distancia

# ------------------------------------------------------------------------------
# 🚩 TODO 4: LOOP PRINCIPAL DA COLÔNIA DE FORMIGAS (CONSTRUÇÃO, EVAPORAÇÃO E ATUALIZAÇÃO)
# ------------------------------------------------------------------------------
def executar_aco():
    global tau
    random.seed(42)
    np.random.seed(42)

    melhor_distancia_global = float('inf')
    melhor_rota_global = []
    historico_melhor_distancia = []
    historico_media_distancia = []

    print("🐜 Iniciando simulação da Colônia de Formigas para as 27 Capitais...")

    for iteracao in range(N_ITERACOES):
        rotas_formigas = []
        distancias_formigas = []

        # 📌 TODO 4.1: Para cada formiga k em N_FORMIGAS:
        # 1. Escolha uma cidade inicial aleatória
        # 2. Enquanto houver cidades nao_visitadas, chame escolher_proxima_cidade()
        # 3. Guarde a rota e a distância calculada com calcular_distancia_rota()

        # === DESENVOLVA AQUI ===
        for k in range(N_FORMIGAS):
            cidade_inicial = random.randrange(N_CIDADES)
            rota = [cidade_inicial]
            nao_visitadas = [c for c in range(N_CIDADES) if c != cidade_inicial]

            while nao_visitadas:
                proxima = escolher_proxima_cidade(rota[-1], nao_visitadas, tau, eta, ALPHA, BETA)
                rota.append(int(proxima))
                nao_visitadas.remove(proxima)

            dist = calcular_distancia_rota(rota)
            rotas_formigas.append(rota)
            distancias_formigas.append(dist)

            # Atualiza o melhor resultado global
            if dist < melhor_distancia_global:
                melhor_distancia_global = dist
                melhor_rota_global = rota[:]

        # 📌 TODO 4.2: Evaporação Global de Feromônio: tau = (1 - RHO) * tau
        # === DESENVOLVA AQUI ===
        tau = (1 - RHO) * tau

        # 📌 TODO 4.3: Deposição de Feromônio pelas formigas nas arestas de suas rotas:
        # Para cada formiga k, delta_tau = Q / dist_k
        # Para cada aresta (u, v) da rota: tau[u][v] += delta_tau e tau[v][u] += delta_tau

        # === DESENVOLVA AQUI ===
        for rota, dist_k in zip(rotas_formigas, distancias_formigas):
            delta_tau = Q / dist_k
            for i in range(len(rota)):
                u = rota[i]
                v = rota[(i + 1) % len(rota)]
                tau[u][v] += delta_tau
                tau[v][u] += delta_tau

        # Rastreamento de métricas
        historico_melhor_distancia.append(melhor_distancia_global)
        historico_media_distancia.append(np.mean(distancias_formigas))

        if (iteracao + 1) % 25 == 0 or iteracao == 0:
            print(f"  Iteração {iteracao+1:03d}/{N_ITERACOES} | Melhor Rota Encontrada: {melhor_distancia_global:.2f} km")

    return melhor_rota_global, melhor_distancia_global, historico_melhor_distancia, historico_media_distancia

# ------------------------------------------------------------------------------
# 🚩 TODO 5: PLOTAGEM GRÁFICA (CURVA DE CONVERGÊNCIA E MAPA DAS CAPITAIS)
# ------------------------------------------------------------------------------
def plotar_resultados(melhor_rota, historico_melhor, historico_media):
    """
    📌 TODO 5.1: Plote dois gráficos lado a lado com Matplotlib:
    - Esquerda: Iterações vs Distância Total (Melhor vs Média do Enxame)
    - Direita: Mapa Geográfico com as 27 Capitais conectadas pela melhor rota ACO.
    """
    # === DESENVOLVA AQUI ===
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Gráfico da esquerda: curva de convergência
    iteracoes = range(1, len(historico_melhor) + 1)
    ax1.plot(iteracoes, historico_melhor, color="green", linewidth=2, label="Melhor global")
    ax1.plot(iteracoes, historico_media, color="orange", linewidth=1.5, label="Média do enxame")
    ax1.set_title("Curva de Convergência do ACO")
    ax1.set_xlabel("Iteração")
    ax1.set_ylabel("Distância total (km)")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Gráfico da direita: mapa com a melhor rota
    coords = [CAPITAIS_BRASIL[LISTA_CIDADES[c]] for c in melhor_rota]
    coords.append(coords[0])  # fecha o circuito
    lons = [c[1] for c in coords]
    lats = [c[0] for c in coords]

    ax2.plot(lons, lats, "-", color="tab:blue", linewidth=1.5, zorder=1)
    ax2.scatter(lons[:-1], lats[:-1], color="red", s=45, zorder=2)
    for idx, c in enumerate(melhor_rota):
        nome = LISTA_CIDADES[c]
        sigla = nome[nome.find("(") + 1:nome.find(")")]
        ax2.annotate(f"{idx + 1}. {sigla}", (lons[idx], lats[idx]),
                     textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax2.scatter(lons[0], lats[0], color="gold", edgecolor="black", s=120, zorder=3, label="Início/Fim")

    ax2.set_title(f"Melhor Rota ACO — {calcular_distancia_rota(melhor_rota):,.0f} km")
    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Latitude")
    ax2.set_aspect("equal", adjustable="datalim")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower right")

    plt.tight_layout()
    plt.savefig("resultado_aco_27_capitais.png", dpi=180, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    print("🐜 Esqueleto do Marco 2 (ACO) carregado com sucesso.")
    print("Implemente os TODOs para executar a simulação da Colônia de Formigas!")
    rota, dist, hist_min, hist_avg = executar_aco()
    plotar_resultados(rota, hist_min, hist_avg)