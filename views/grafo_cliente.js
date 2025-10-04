const URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", function() {
    geraImagemGrafo();
    
});

document.getElementById("searchForm").addEventListener("submit", function(event) {
    encontrarCaminho(event);
});
document.getElementById("methodSelect").addEventListener("change", function(event){
      if(this.value == "profundidade" || this.value=="prof_limitada"){
           const divLimite = document.getElementById("limite")
           const label  = document.getElementById("number");
            divLimite.style.display = "block"

             if(this.value == "profundidade"){
                 label.innerText="Limite"
             }else{
                 label.innerText = "Limite Máximo"
             }
          
      }
})
document.querySelectorAll("input[name='grafo']").forEach(radio => {
    radio.addEventListener("change", function() {
        const tipoGrafo = this.value;
        geraImagemGrafo(tipoGrafo);
    });
});
function geraImagemGrafo(tipoGrafo="grafo_sem_pesos") {
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
    const method = document.getElementById("methodSelect").value;
     const limiteInput = document.getElementById("number");
    let limite;
   if (limiteInput.value && limiteInput) {
    limite = parseInt(limiteInput.value, 10);
}
    const loader = document.getElementById("loader");
    loader.style.display = "block"; 
    document.getElementById("container").style.opacity = "0";
    debugger;

    fetch(URL + "/calcular-rota", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ start: startVertex, end: endVertex, method: method, ...(limite !== undefined ? { limite } : {}) })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById("caminho").innerText = data.valores;
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

