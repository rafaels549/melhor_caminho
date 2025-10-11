from collections import deque
from NodeP import NodeP

class buscaP(object):
#--------------------------------------------------------------------------
# SUCESSORES PARA GRAFO
#--------------------------------------------------------------------------
    def sucessores_grafo(self,ind,grafo,ordem):
        
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
    
#--------------------------------------------------------------------------
# SUCESSORES PARA GRID
#--------------------------------------------------------------------------
    def sucessores_grid(self,st,nx,ny,mapa):
        f = []
        x, y = st[0], st[1]
        # DIREITA
        if y+1<ny:
            if mapa[x][y+1]==0:
                suc = []
                suc.append(x)
                suc.append(y+1)
                custo = 5
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ESQUERDA
        if y-1>=0:
            if mapa[x][y-1]==0:
                suc = []
                suc.append(x)
                suc.append(y-1)
                custo = 7
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ABAIXO
        if x+1<nx:
            if mapa[x+1][y]==0:
                suc = []
                suc.append(x+1)
                suc.append(y)
                custo = 2
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)
        # ACIMA
        if x-1>=0:
            if mapa[x-1][y]==0:
                suc = []
                suc.append(x-1)
                suc.append(y)
                custo = 29
                aux = []
                aux.append(suc)
                aux.append(custo)
                f.append(aux)        
        return f
#--------------------------------------------------------------------------    
# INSERE NA LISTA MANTENDO-A ORDENADA
#--------------------------------------------------------------------------    
    def inserir_ordenado(self,lista, no):
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                break
        else:
            lista.append(no)
#--------------------------------------------------------------------------    
# EXIBE O CAMINHO ENCONTRADO NA ÁRVORE DE BUSCA
#--------------------------------------------------------------------------    
    def exibirCaminho(self,node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho
#--------------------------------------------------------------------------    
# GERA H DE FORMA ALEATÓRIA
#--------------------------------------------------------------------------    
    def heuristica_grafo(self, nos, destino, n, grafo):
        """
        Estima o custo do nó `n` até o `destino` usando:
        h(n) = menor_peso * numero_minimo_de_arestas
        """
        # 1. Descobre o menor peso de todas as arestas do grafo
        menor_peso = float('inf')
        for adj in grafo:
            for _, peso in adj:
                if peso < menor_peso:
                    menor_peso = peso

        # 2. Calcula o número mínimo de arestas até o destino usando BFS
        inicio = n
        fim = destino
        fila = deque([(inicio, 0)])
        visitado = set([inicio])
        
        while fila:
            atual, passos = fila.popleft()
            if atual == fim:
                return menor_peso * passos  # custo estimado conservador
            i_atual = nos.index(atual)   # <-- pegar índice no array de grafo
            for vizinho, _ in grafo[i_atual]:
                if vizinho not in visitado:
                    visitado.add(vizinho)
                    fila.append((vizinho, passos + 1))
        
        # se não houver caminho conhecido, retorna uma heurística grande
        return menor_peso * len(grafo)
# -----------------------------------------------------------------------------
# CUSTO UNIFORME
# -----------------------------------------------------------------------------
    #def custo_uniforme(self,inicio,fim,mapa,nx,ny):
    def custo_uniforme(self, inicio, fim, nos, grafo): #grafo
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        #t_inicio = tuple(inicio)   # grid
        raiz = NodeP(None, inicio, 0, None, None, 0) # grafo
       # raiz = NodeP(None, t_inicio,0, None, None, 0)  # grid
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        #visitado = {tuple(inicio): raiz}    # grid
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo: UCS garante ótimo (custos >= 0)
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
            
            # Gera sucessores a partir do grid
           #filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid
    
            for novo in filhos: # grafo
            #for novo in filhos: # grid
                # custo acumulado até o sucessor
               
                v2 = valor_atual + novo[1]
                v1 = v2 
    
                # Não visitado ou custo melhor
                #t_novo = tuple(novo[0])       # grid
                #if (t_novo not in visitado) or (v2<visitado[t_novo].v2): # grid
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    #filho = NodeP(atual,t_novo, v1, None, None, v2) # grid
                    filho = NodeP(atual, novo[0], v1, None, None, v2) # grafo
                    visitado[novo[0]] = filho #grafo
                    #visitado[t_novo] = filho # grid
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None
# -----------------------------------------------------------------------------
# GREEDY
# -----------------------------------------------------------------------------
    def greedy(self, inicio, fim, nos, grafo):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        raiz = NodeP(None, inicio, 0, None, None, 0)
    
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Se já registramos um nó melhor para este estado, este está obsoleto
            #if visitado.get(atual.estado) is not atual:
            #    continue
    
            # Chegou ao objetivo: UCS garante ótimo (custos >= 0)
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
    
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = self.heuristica_grafo(nos,novo[0],fim, grafo) 
    
                # relaxamento: nunca visto ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2)
                    visitado[novo[0]] = filho
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None  
# -----------------------------------------------------------------------------
# A ESTRELA
# -----------------------------------------------------------------------------
    def a_estrela(self,inicio,fim,nos,grafo,):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        raiz = NodeP(None, inicio, 0, None, None, 0)
    
        lista.append(raiz)
    
        # Controle de nós visitados
        visitado = {inicio: raiz}
        
        # loop de busca
        while lista:
            # remove o primeiro nó
            atual = lista.popleft()
            valor_atual = atual.v2
    
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self.exibirCaminho(atual)
                return caminho, atual.v2
    
            # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
            ind = nos.index(atual.estado)
            filhos = self.sucessores_grafo(ind, grafo, 1)
    
            for novo in filhos:
                # custo acumulado até o sucessor
                v2 = valor_atual + novo[1]
                v1 = v2 + self.heuristica_grafo(nos,novo[0],fim,grafo) 
    
                # relaxamento: nunca visto ou custo melhor
                if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                    filho = NodeP(atual, novo[0], v1, None, None, v2)
                    visitado[novo[0]] = filho
                    self.inserir_ordenado(lista, filho)
    
        # Sem caminho
        return None
# -----------------------------------------------------------------------------
# AI ESTRELA
# -----------------------------------------------------------------------------       
    def aia_estrela(self,inicio,fim,nos,grafo):
        # Origem igual a destino
        if inicio == fim:
            return [inicio]
        
        limite = self.heuristica_grafo(nos,inicio,fim, grafo) 
        # Fila de prioridade baseada em deque + inserção ordenada
        lista = deque()
        
        # Busca iterativa
        while True:
            lim_acima = []
            
            raiz = NodeP(None, inicio, 0, None, None, 0)       
            lista.append(raiz)
        
            # Controle de nós visitados
            visitado = {inicio: raiz}

            while lista:
                # remove o primeiro nó
                atual = lista.popleft()
                valor_atual = atual.v2
                
                # Chegou ao objetivo
                if atual.estado == fim:
                    caminho = self.exibirCaminho(atual)
                    return caminho, atual.v2, limite
                
                # Gera sucessores; esperado: [(estado_suc, custo_aresta), ...]
                ind = nos.index(atual.estado)
                filhos = self.sucessores_grafo(ind, grafo, 1)
                
                for novo in filhos:
                    # custo acumulado até o sucessor
                    v2 = valor_atual + novo[1]
                    v1 = v2 + self.heuristica_grafo(nos,novo[0],fim) 
                    
                    # Verifica se está dentro do limite
                    if v1<=limite:
                        # Não visitado ou custo melhor
                        if (novo[0] not in visitado) or (v2 < visitado[novo[0]].v2):
                            filho = NodeP(atual, novo[0], v1, None, None, v2)
                            visitado[novo[0]] = filho
                            self.inserir_ordenado(lista, filho)
                    else:
                        lim_acima.append(v1)
            
            limite = sum(lim_acima)/len(lim_acima)
            lista.clear()
            visitado.clear()
            filhos.clear()
                        
        return None
