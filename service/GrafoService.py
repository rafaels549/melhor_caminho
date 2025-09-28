import networkx as nx
import matplotlib.pyplot as plt
from BuscaNP import buscaNP
import io
import base64
from pathlib import Path

class GrafoService:
   import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from pathlib import Path
from BuscaNP import buscaNP  # ou ajuste se for função

class GrafoService:
    def __init__(self):
        self.G = nx.Graph()
        self.pos = {}

        # Caminho do arquivo de adjacência
        file_path = Path(__file__).parent.parent / "data" / "lista de adjacencia.txt"

        # Lê a lista de adjacência
        listaDeAdjacencia = {}
        nos = set()

        with open(file_path, "r", encoding="utf-8") as f:
            linhas = f.readlines()

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

        nos = list(nos)

        # Cria o grafo NetworkX
        for i, filhos in enumerate([listaDeAdjacencia.get(no, []) for no in nos]):
            pai = nos[i]
            for f in filhos:
                self.G.add_edge(pai, f)

        # Calcula layout para todos os nós
        self.pos = nx.spring_layout(self.G, seed=42)

    def gera_grafo(self):
        plt.figure(figsize=(6,4))
        nx.draw(self.G, self.pos, with_labels=True, node_color="lightgray", edge_color="gray", node_size=500)
        plt.axis("off")

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        plt.close()
        buf.seek(0)
        return {"image_base64": base64.b64encode(buf.getvalue()).decode("utf-8")}
    

    def calcular_rota(self, start, end, method):
        # Lógica para calcular a rota com base nos parâmetros recebidos
        nos, grafo = self.gerar_lista_adjacencia()

         # Faz a busca
        busca = buscaNP()

        caminho = getattr(busca, method)(start, end, nos, grafo)
        caminho_imagem = self._desenhar_caminho(caminho)
        return {"valores": caminho, "imagem_base64": caminho_imagem}

    def gerar_lista_adjacencia(self):
        listaDeAdjacencia = {}  # dicionário temporário
        nos = set()

        file_path = Path(__file__).parent.parent / "data" / "lista de adjacencia.txt"

        with open(file_path, "r", encoding="utf-8") as f:
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

        return nos, grafo
    
    def _desenhar_caminho(self, caminho):
        plt.figure(figsize=(6,4))

        # desenha o grafo normal
        nx.draw(self.G, self.pos, with_labels=True,
                node_color="lightgray", edge_color="gray",
                node_size=500)

        # destacar nós do caminho
        nx.draw_networkx_nodes(
            self.G, self.pos,
            nodelist=caminho,
            node_color="lightgreen",
            node_size=600
        )

        # destacar arestas do caminho
        edges = list(zip(caminho, caminho[1:]))
        nx.draw_networkx_edges(
            self.G, self.pos,
            edgelist=edges,
            edge_color="red",
            width=2
        )

        plt.axis("off")
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
