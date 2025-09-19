from BuscaNP import buscaNP

def main():
    listaDeAdjacencia = {}  # dicionário temporário
    nos = set()

    # Lê o arquivo
    with open("lista de adjacencia.txt", "r", encoding="utf-8") as f:
        linhas = f.readlines()

    # Monta dicionário e conjunto de nós
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        partes = linha.split(",")
        pai = partes[0].strip()
        filhos = [f.strip() for f in partes[1:]]

        listaDeAdjacencia[pai] = filhos
        nos.add(pai)
        for f in filhos:
            nos.add(f)

    nos = list(nos)  # converte set para lista

    # Cria a "lista de listas" que buscaNP espera
    grafo = []
    for no in nos:
        # adiciona os filhos se existirem, senão adiciona lista vazia
        grafo.append(listaDeAdjacencia.get(no, []))

    # Mostra para conferir
    print("Nós:", nos)
    print("Grafo (lista de listas):")
    for i, filhos in enumerate(grafo):
        print(f"{nos[i]} -> {filhos}")

    # Faz a busca
    buscador = buscaNP()
    inicio = 'a'  # nó inicial
    fim = 'g'     # nó objetivo
    caminho = buscador.amplitude(inicio, fim, nos, grafo)

    print("\nCaminho encontrado:", caminho)

if __name__ == "__main__":
    main()
