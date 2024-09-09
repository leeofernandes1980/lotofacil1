import csv
import random
import pandas as pd

# Função para gerar combinações com base nas dezenas mais sorteadas
def gerar_combinacoes(dezenas_mais_sorteadas, total_dezenas, num_combinacoes, dados_concursos):
    combinacoes = []
    num_concursos = len(dados_concursos)
    
    for _ in range(num_combinacoes):
        # Dezenas repetidas
        percentual_repetidas = random.random()  # Gere um valor aleatório entre 0 e 1
        if percentual_repetidas <= 0.5:
            numeros_repetidos = 10
        elif percentual_repetidas <= 0.8:
            numeros_repetidos = 9
        else:
            numeros_repetidos = 8

        # Pares e ímpares
        percentual_pares_impares = random.random()
        if percentual_pares_impares <= 0.3:
            pares = 8
        elif percentual_pares_impares <= 0.6:
            pares = 7
        else:
            pares = 6

        impares = total_dezenas - pares

        # Crie uma combinação com base nos critérios
        combinacao = []
        while len(combinacao) < total_dezenas:
            for numero in dezenas_mais_sorteadas:
                if numeros_repetidos > 0 and numero not in combinacao:
                    combinacao.append(numero)
                    numeros_repetidos -= 1
                elif pares > 0 and numero % 2 == 0 and numero not in combinacao:
                    combinacao.append(numero)
                    pares -= 1
                elif impares > 0 and numero % 2 != 0 and numero not in combinacao:
                    combinacao.append(numero)
                    impares -= 1

        random.shuffle(combinacao)  # Embaralhe as dezenas para garantir aleatoriedade
        combinacao = sorted(combinacao[:total_dezenas])  # Mantenha apenas as 15 dezenas
        combinacoes.append(combinacao)

    return combinacoes

# Função para contar as vezes que a combinação foi sorteada com 12, 13, 14 ou 15 dezenas
def contar_sorteios(comb, resultados):
    contagem = {
        12: 0,
        13: 0,
        14: 0,
        15: 0
    }

    for resultado in resultados:
        numeros_sorteados = set(map(int, resultado.split(",")))
        acertos_comb = set(comb).intersection(numeros_sorteados)
        quantidade_acertos = len(acertos_comb)

        if quantidade_acertos >= 12:
            contagem[quantidade_acertos] += 1

    return contagem

# Função para obter as dezenas não sorteadas nos últimos 3 concursos
def dezenas_nao_sorteadas(resultados, ultimos_concursos=3):
    dezenas_sorteadas = set()
    
    for resultado in resultados[:ultimos_concursos]:  # Considerar apenas os últimos concursos
        numeros_sorteados = set(map(int, resultado.split(",")))
        dezenas_sorteadas.update(numeros_sorteados)
    
    todas_dezenas = set(range(1, 26))
    dezenas_nao_sorteadas = todas_dezenas - dezenas_sorteadas
    
    return sorted(list(dezenas_nao_sorteadas))

# Função para verificar se um número é primo
def is_primo(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Função para contar pares, ímpares, números de Fibonacci e repetições
def contar_caracteristicas(comb):
    pares = len([x for x in comb if x % 2 == 0])
    impares = len([x for x in comb if x % 2 != 0])
    fibonacci = len([x for x in comb if is_primo(x) and x > 1])
    repeticoes = len(comb) - len(set(comb))
    
    return pares, impares, fibonacci, repeticoes

# Carregue os resultados do arquivo CSV
resultados = []

with open(r"C:\localizaçãodoarquivo\lotofacilatual1.csv", 'r') as arquivo:
    linhas = csv.reader(arquivo)
    for linha in linhas:
        resultado = ",".join(linha)
        resultados.append(resultado)

# Dados sobre os últimos 10 concursos
dados_concursos = [
    {"repetidas": 10, "pares": 8, "impares": 7},
    {"repetidas": 9, "pares": 7, "impares": 8},
    {"repetidas": 8, "pares": 6, "impares": 9},
]

# Defina o número total de dezenas e o número de combinações desejadas
total_dezenas = 17  # Escolha o número de dezenas para suas combinações
num_combinacoes = 1000 # Ou o número que desejar

# Calcule as dezenas mais sorteadas (substitua pela lista de dezenas mais sorteadas)
dezenas_mais_sorteadas = list(range(1, 26))

# Obtenha as dezenas não sorteadas nos últimos 3 concursos
dezenas_nao_sorteadas_ultimos_3 = dezenas_nao_sorteadas(resultados, ultimos_concursos=3)

# Obtenha as dezenas mais sorteadas nos últimos 20 concursos
def obter_dezenas_mais_sorteadas_ultimos_20(resultados, ultimos_sorteios=20):
    dezenas_sorteadas = {}
    
    for resultado in resultados[:ultimos_sorteios]:
        numeros_sorteados = list(map(int, resultado.split(",")))
        for numero in numeros_sorteados:
            if numero in dezenas_sorteadas:
                dezenas_sorteadas[numero] += 1
            else:
                dezenas_sorteadas[numero] = 1

    # Ordenar as dezenas por número de ocorrências em ordem decrescente
    dezenas_ordenadas = sorted(dezenas_sorteadas.items(), key=lambda x: x[1], reverse=True)

    return [dezena for dezena, _ in dezenas_ordenadas[:10]]

dezenas_mais_sorteadas_20 = obter_dezenas_mais_sorteadas_ultimos_20(resultados)

# Gere as combinações de jogos com base nas novas informações
combinacoes = gerar_combinacoes(dezenas_mais_sorteadas, total_dezenas, num_combinacoes, dados_concursos)

# Crie um DataFrame com as informações
data = []
for i, combinacao in enumerate(combinacoes, start=1):
    contagem = contar_sorteios(combinacao, resultados)
    pares, impares, fibonacci, repeticoes = contar_caracteristicas(combinacao)
    dezenas_nao_sorteadas_ultimos_3_str = ", ".join(map(str, dezenas_nao_sorteadas_ultimos_3))
    dezenas_mais_sorteadas_20_str = ", ".join(map(str, dezenas_mais_sorteadas_20))
    
    data.append([i, combinacao, contagem[12], contagem[13], contagem[14], contagem[15], pares, impares, fibonacci, repeticoes, dezenas_nao_sorteadas_ultimos_3_str, dezenas_mais_sorteadas_20_str])

# Crie um DataFrame com as informações
df = pd.DataFrame(data, columns=["Combinação", "Dezenas", "12 Dezenas", "13 Dezenas", "14 Dezenas", "15 Dezenas", "Pares", "Ímpares", "Fibonacci", "Repetições", "Dezenas Não Sorteadas (Últimos 3)", "Dezenas Mais Sorteadas (Últimos 20)"])

# Exporte o DataFrame para um arquivo CSV
df.to_csv(r"C:\pastaondeserá salvo o arquivo\lotofacil_info.csv", index=False)
