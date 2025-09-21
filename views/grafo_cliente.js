const URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", function() {
    geraImagemGrafo();
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
