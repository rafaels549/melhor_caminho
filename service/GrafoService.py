import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

class GrafoService:
    def __init__(self):
        self.G = nx.Graph()
        self.G.add_edges_from([(1, 2), (2, 3), (3, 4)])
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
    

    def calcular_rota(self):
        return {"hello": "world"}


