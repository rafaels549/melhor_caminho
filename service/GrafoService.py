import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from pathlib import Path
from BuscaNP import buscaNP
from BuscaP import buscaP
from ag_pcv import AlgoritmoGenetico
from subida_encosta import (SubidaEncosta, SubidaEncostaLimite)
from tempera_simulada import TemperaSimulada
import numpy as np


class GrafoService:
    
    _grafo = None
    _pos = None
    _nos = None
    _lista_adjacencia = None
    _tipoGrafo  = None
    _matriz = None
    ganhos = {
    "SE" :{
        "ganho_total": [],
        "num_execucoes": [],
        "tamanho_populacao": []
    },
    "SEL" :{
        "ganho_total": [],
        "num_execucoes": [],
        "configuracoes": [],
        "tamanho_populacao": []
    },
    "TS" :{
        "ganho_total": [],
        "num_execucoes": [],
        "configuracoes": [],
        "tamanho_populacao": []
    },
    "AG" :{
        "ganho_total": [],
        "num_execucoes": [],
        "configuracoes": [],
        "tamanho_populacao": []
    }
}

    def __init__(self, tipoGrafo=None):
        if GrafoService._grafo is None or tipoGrafo != GrafoService._tipoGrafo:
            self.carregar_grafo(tipoGrafo)


    def converter_para_python(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()          # array -> lista
        elif isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)              # numpy int -> int normal
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)            # numpy float -> float normal
        elif isinstance(obj, (list, tuple)):
            return [self.converter_para_python(x) for x in obj]  # recursivo para listas/tuplas
        elif isinstance(obj, dict):
            return {k: self.converter_para_python(v) for k, v in obj.items()}  # recursivo para dict
        else:
            return obj

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
        nx.draw(GrafoService._grafo, self._pos, with_labels=True, node_color="lightgray",
                edge_color="gray", node_size=500)
         # Desenha os pesos das arestas
        if self._tipoGrafo == "grafo_com_pesos":
            edge_labels = nx.get_edge_attributes(GrafoService._grafo, "weight")
            nx.draw_networkx_edge_labels(
            GrafoService._grafo,
            self._pos,
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

    def calcular_rota(self, start, end, method, tipoGrafo, limite=None):
        nos, grafo = self.gerar_lista_adjacencia()

        if tipoGrafo == "grafo_com_pesos":
            busca = buscaP()
        else:
            busca = buscaNP()
        if limite is not None:
            caminho = getattr(busca, method)(start, end, nos, grafo, limite)
        else:
            caminho = getattr(busca, method)(start, end, nos, grafo)
        if not caminho:
            return {"valores": ["Erro ao fazer busca, caminho não encontrado"], "imagem_base64": None}
        caminho_imagem = self._desenhar_caminho(caminho, tipoGrafo)
        if(tipoGrafo == "grafo_com_pesos" ):
            if(method == "aia_estrela"):
                return {"valores": caminho[0], "custo_total": caminho[1], "limite": caminho[2], "imagem_base64": caminho_imagem}
            return {"valores": caminho[0], "custo_total": caminho[1], "imagem_base64": caminho_imagem}
        
        return {"valores": caminho, "imagem_base64": caminho_imagem}

    def gerar_lista_adjacencia(self):
        
        nos = self._nos
        listaDeAdjacencia = self._lista_adjacencia
      
        grafo = []
        for no in nos:
            grafo.append(listaDeAdjacencia.get(no, []))
        
        return nos, grafo

    def _desenhar_caminho(self, caminho_com_custo, tipoGrafo):
        plt.figure(figsize=(10, 8))

        # Se for tupla (caminho, custo_total), separa
        if isinstance(caminho_com_custo, tuple):
            caminho = caminho_com_custo[0]
        else:
            caminho = caminho_com_custo

        # Desenha o grafo base
        nx.draw(
            GrafoService._grafo, self._pos,
            with_labels=True,
            node_color="lightgray",
            edge_color="gray",
            node_size=500
        )

        # Destaca os nós do caminho
        nx.draw_networkx_nodes(
            GrafoService._grafo, self._pos,
            nodelist=caminho,
            node_color="lightgreen",
            node_size=600
        )

        # Destaca as arestas do caminho
        edges = list(zip(caminho, caminho[1:]))
        nx.draw_networkx_edges(
            GrafoService._grafo, self._pos,
            edgelist=edges,
            edge_color="red",
            width=2
        )

        # Se for grafo com pesos, exibe os pesos
        if tipoGrafo == "grafo_com_pesos":
            edge_labels = nx.get_edge_attributes(GrafoService._grafo, "weight")
            nx.draw_networkx_edge_labels(
                GrafoService._grafo,
                self._pos,
                edge_labels=edge_labels,
                font_size=9,
                label_pos=0.5,
                rotate=False,
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.8)
            )

        plt.axis("off")

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    

    
    def calcular_caminho_bl(self, metodo, mat, tp, ng, tc, tm, ig, limite=None, t_ini=None, t_fim=None, fr=None):
       
        if metodo == "AlgoritimoGenetico":
            si, sf, vi, vf = AlgoritmoGenetico(len(mat), mat, tp, ng, tc, tm, ig)


            GrafoService.ganhos['AG']["num_execucoes"].append(len(GrafoService.ganhos['AG']["num_execucoes"]) + 1)
            GrafoService.ganhos['AG']["configuracoes"].append({
                "tp": tp,
                "ng": ng,
                "tc": tc,
                "tm": tm,
            })
            GrafoService.ganhos['AG']["ganho_total"].append(100*abs((vf - vi))/vi)
            GrafoService.ganhos['AG']["tamanho_populacao"].append(len(mat))
            
        if metodo == "SubidaEncosta":
            sf, vf, si, vi = SubidaEncosta(len(mat), mat)
            GrafoService.ganhos['SE']["ganho_total"].append(100*abs((vf - vi))/vi)
            GrafoService.ganhos['SE']["tamanho_populacao"].append(len(mat))
            GrafoService.ganhos['SE']["num_execucoes"].append(len(GrafoService.ganhos['SE']["num_execucoes"]) + 1)
           
        if metodo == "SubidaEncostaLimite":
            sf, vf,si, vi = SubidaEncostaLimite(len(mat), mat, limite) 
            GrafoService.ganhos['SEL']["ganho_total"].append(100*abs((vf - vi))/vi)   
            GrafoService.ganhos['SEL']["num_execucoes"].append(len(GrafoService.ganhos['SEL']["num_execucoes"]) + 1)
            GrafoService.ganhos['SEL']["tamanho_populacao"].append(len(mat))
            GrafoService.ganhos['SEL']["configuracoes"].append({
                "limite": limite,
            })
        if metodo == "TemperaSimulada":
            si, vi, sf, vf = TemperaSimulada(len(mat), mat, t_ini, t_fim, fr)
            GrafoService.ganhos['TS']["ganho_total"].append(100*abs((vf - vi))/vi)   
            GrafoService.ganhos['TS']["num_execucoes"].append(len(GrafoService.ganhos['TS']["num_execucoes"]) + 1)
            GrafoService.ganhos['TS']["tamanho_populacao"].append(len(mat))
            GrafoService.ganhos['TS']["configuracoes"].append({
                "initial_temp": t_ini,
                "final_temp": t_fim,
                "cooling_rate": fr
            })    
        
        resultado = {
        "si": si,
        "sf": sf,
        "vi": vi,
        "vf": vf,
    }

        resultado_convertido = self.converter_para_python(resultado)

        return {"resultado": resultado_convertido}
    def gerar_relatorio(self):
        return GrafoService.ganhos