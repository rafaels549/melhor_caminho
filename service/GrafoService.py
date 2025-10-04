import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from pathlib import Path
from BuscaNP import buscaNP


class GrafoService:
    
    _grafo = None
    _pos = None
    _nos = None
    _lista_adjacencia = None
    _tipoGrafo  = None

    def __init__(self, tipoGrafo=None):
        if GrafoService._grafo is None or tipoGrafo != GrafoService._tipoGrafo or tipoGrafo is None:
            self.carregar_grafo(tipoGrafo)

        self.G = GrafoService._grafo
        self.pos = GrafoService._pos
        self.nos = GrafoService._nos
        self.lista_adjacencia = GrafoService._lista_adjacencia
        self.tipoGrafo = tipoGrafo

    def carregar_grafo(self, tipoGrafo=None):
        # Define arquivo a ser carregado
        if tipoGrafo == "grafo_com_pesos":
            file_path = Path(__file__).parent.parent / "data" / "lista_de_ajacencia_pesos.txt"
        else:
            file_path = Path(__file__).parent.parent / "data" / "lista de adjacencia.txt"

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

            if tipoGrafo == "grafo_com_pesos":
                filhos = []
                # percorre de 2 em 2: [vizinho, peso]
                filhos_e_pesos = partes[1:]
                for i in range(0, len(filhos_e_pesos), 2):
                    filho = filhos_e_pesos[i].strip()
                    peso = int(filhos_e_pesos[i + 1].strip())
                    filhos.append((filho, peso))
                    nos.add(filho)
                listaDeAdjacencia[pai] = filhos
            else:
                # grafo sem pesos
                filhos = [f.strip() for f in partes[1:]]
                listaDeAdjacencia[pai] = filhos
                for f in filhos:
                    nos.add(f)

            nos.add(pai)

        nos = sorted(list(nos))
        G = nx.Graph()

        # Adiciona arestas
        for no in nos:
            filhos = listaDeAdjacencia.get(no, [])
            if tipoGrafo == "grafo_com_pesos":
                for f, peso in filhos:
                    G.add_edge(no, f, weight=peso)
            else:
                for f in filhos:
                    G.add_edge(no, f)

        GrafoService._grafo = G
        GrafoService._pos = nx.spring_layout(G, seed=42 ,k=5.0)
        GrafoService._nos = nos
        GrafoService._lista_adjacencia = listaDeAdjacencia
        GrafoService._tipoGrafo = tipoGrafo

    def gera_grafo(self):
        plt.figure(figsize=(10, 8))
        nx.draw(self.G, self.pos, with_labels=True, node_color="lightgray",
                edge_color="gray", node_size=500)
         # Desenha os pesos das arestas
        if self.tipoGrafo == "grafo_com_pesos":
            edge_labels = nx.get_edge_attributes(self.G, "weight")
            nx.draw_networkx_edge_labels(
            self.G,
            self.pos,
            edge_labels=edge_labels,
            font_size=9,
            label_pos=0.5, 
            rotate= False,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8)  # fundo branco transparente
            )
            plt.axis("off")

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        plt.close()
        buf.seek(0)
        return {"image_base64": base64.b64encode(buf.getvalue()).decode("utf-8")}

    def calcular_rota(self, start, end, method, limite=None):
        nos, grafo = self.gerar_lista_adjacencia()

    
        busca = buscaNP()
        if limite is not None:
            caminho = getattr(busca, method)(start, end, nos, grafo, limite)
        else:
            caminho = getattr(busca, method)(start, end, nos, grafo)
        if not caminho:
            return {"valores": ["Erro ao fazer busca, caminho não encontrado"], "imagem_base64": None}
        caminho_imagem = self._desenhar_caminho(caminho)
        return {"valores": caminho, "imagem_base64": caminho_imagem}

    def gerar_lista_adjacencia(self):
        
        nos = self.nos
        listaDeAdjacencia = self.lista_adjacencia

        grafo = []
        for no in nos:
            grafo.append(listaDeAdjacencia.get(no, []))

        return nos, grafo

    def _desenhar_caminho(self, caminho):
        plt.figure(figsize=(6, 4))

        
        nx.draw(self.G, self.pos, with_labels=True,
                node_color="lightgray", edge_color="gray",
                node_size=500)

        
        nx.draw_networkx_nodes(
            self.G, self.pos,
            nodelist=caminho,
            node_color="lightgreen",
            node_size=600
        )

    
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
