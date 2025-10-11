const URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", function() {
    geraImagemGrafo();
    
    
});

document.getElementById("searchForm").addEventListener("submit", function(event) {
    encontrarCaminho(event);
});
document.getElementById("methodSelect").addEventListener("change", function(event){
       const divLimite = document.getElementById("limite")
       const label  = document.getElementById("labelNumber");
      if(this.value == "prof_limitada" || this.value=="aprof_iterativo"){
        
            divLimite.style.display = "block"

             if(this.value == "prof_limitada"){
                 label.innerText="Limite"
             }else{
                 label.innerText = "Limite Máximo"
             }
          
      }else{
            divLimite.style.display = "none"
      }
})
document.querySelectorAll("input[name='grafo']").forEach(radio => {
    radio.addEventListener("change", function() {
        const caminho = document.getElementById("caminho");
        const graphImg = document.getElementById("graphContainer").querySelector("img");
        const resultContainer = document.getElementById("resultContainer");
      
        caminho.innerText = "";
        if (graphImg) graphImg.removeAttribute("src");
        if (resultContainer) resultContainer.innerHTML = "";
        const tipoGrafo = this.value;
        geraImagemGrafo(tipoGrafo);
    });
});
function geraImagemGrafo(tipoGrafo="grafo_sem_pesos") {
    if(tipoGrafo === "grafo_com_pesos"){
        document.getElementById("methodSelect").style.display = "none";
        document.getElementById("methodSelect2").style.display = "block";
    }else{
        document.getElementById("methodSelect").style.display = "block";
        document.getElementById("methodSelect2").style.display = "none";
    }
    const loader = document.getElementById("loader");
    loader.style.display = "block"; // mostra loader
    document.getElementById("container").style.opacity = "0"; // escurece container
    fetch(URL + "/gera_grafo?name=" + tipoGrafo)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const img = document.createElement("img");
            img.src = "data:image/png;base64," + data.image_base64;
            document.getElementById("graphContainer").innerHTML = "";
            document.getElementById("graphContainer").appendChild(img);
        })
        .catch(err => console.error("Erro ao gerar grafo:", err))
        .finally(() => {
            loader.style.display = "none"; // esconde loader
            document.getElementById("container").style.opacity = "1"; // volta normal
        });
}

function encontrarCaminho(event) {
    event.preventDefault();
    const startVertex = document.getElementById("startVertex").value;
    const endVertex = document.getElementById("endVertex").value;
     let tipoGrafo = "grafo_sem_pesos";
    document.querySelectorAll("input[name='grafo']").forEach(radio => {
        if (radio.checked) {
            tipoGrafo = radio.value;
        }
    });
    
    let methodSelect;
    if(tipoGrafo === "grafo_com_pesos"){
        methodSelect = document.getElementById("methodSelect2");
    }else{
        methodSelect = document.getElementById("methodSelect");
    }
    const method = methodSelect.value;

     const limiteInput = document.getElementById("number");
    let limite;
   if (limiteInput.value && limiteInput) {
    limite = parseInt(limiteInput.value, 10);
}
    const loader = document.getElementById("loader");
    loader.style.display = "block"; 
    document.getElementById("container").style.opacity = "0";
   

    fetch(URL + "/calcular-rota", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ start: startVertex, end: endVertex, method: method, ...(limite !== undefined ? { limite } : {}), tipoGrafo: tipoGrafo })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const caminho = document.getElementById("caminho");
        caminho.innerText = "";
        caminho.innerText += data.valores;
        if (data.custo_total) {
              caminho.innerText += " Custo total: " + data.custo_total;
        }
        if (data.limite) {
            caminho.innerText += " Limite " + data.limite;
        }
        const img = document.createElement("img");
        img.src = "data:image/png;base64," + data.imagem_base64;
        document.getElementById("resultContainer").innerHTML = "";
        document.getElementById("resultContainer").appendChild(img);
    })
    .catch(err => console.error("Erro ao iniciar busca:", err))
    .finally(() => {
        loader.style.display = "none";
        document.getElementById("container").style.opacity = "1";
    });
}

