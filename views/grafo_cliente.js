const URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", function() {
    geraImagemGrafo();
});

document.getElementById("searchForm").addEventListener("submit", function(event) {

    encontrarCaminho(event);

});

  function geraImagemGrafo() {
            fetch(URL + "/gera_grafo")
                .then(response => response.json())
                .then(data => {
                    const img = document.createElement("img");
                    img.src = "data:image/png;base64," + data.image_base64;
                    document.getElementById("graphContainer").innerHTML = "";
                    document.getElementById("graphContainer").appendChild(img);
                })
                .catch(err => console.error("Erro ao gerar grafo:", err));
        }

  function encontrarCaminho(event) {
    event.preventDefault(); // Evita o envio padrão do formulário      

    const startVertex = document.getElementById("startVertex").value;
    const endVertex = document.getElementById("endVertex").value;
    const method = document.getElementById("methodSelect").value;

    fetch(URL + "/calcular-rota", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            start: startVertex,
            end: endVertex,
            method: method
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("caminho").innerText = data.caminho;
        const img = document.createElement("img");
        img.src = "data:image/png;base64," + data.imagem_base64;
        document.getElementById("resultContainer").innerHTML = "";
        document.getElementById("resultContainer").appendChild(img);
    })
    .catch(err => console.error("Erro ao iniciar busca:", err));
}
