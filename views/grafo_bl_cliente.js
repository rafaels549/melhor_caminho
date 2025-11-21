const URL = "http://127.0.0.1:8000";
document.addEventListener("DOMContentLoaded", function() {
});

document.getElementById("methodSelect").addEventListener("change", function(event){
    event.preventDefault();
    IniciarValoresBuscaLocalMetaheuristicas(event);
});
function gerarPDF() {
    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    doc.setFontSize(16);
    doc.text("Relatório de Ganhos Percentuais Médios", 14, 15);

    doc.autoTable({
        html: "#relatorioTable",   // id da tabela HTML
        startY: 25,
        theme: "grid",
        styles: { fontSize: 10 },
    });

    doc.save("relatorio_ganhos.pdf");
}

function IniciarValoresBuscaLocalMetaheuristicas(event) {
    
    if (event.target.value  === "AlgoritimoGenetico") {
        document.getElementById("genetic_parameters").style.display = "block";
        document.getElementById("tempera").style.display = "none";
        document.getElementById("limite").style.display = "none";
      
    } else if (event.target.value === "SubidaEncostaLimite") {
        document.getElementById("limite").style.display = "block";
        document.getElementById("tempera").style.display = "none";
        document.getElementById("genetic_parameters").style.display = "none";
    

    } else if (event.target.value === "TemperaSimulada") {
        document.getElementById("tempera").style.display = "block";
        document.getElementById("genetic_parameters").style.display = "none";
        document.getElementById("limite").style.display = "none";


    } else {
        document.getElementById("genetic_parameters").style.display = "none";
        document.getElementById("limite").style.display = "none";
        document.getElementById("tempera").style.display = "none";
    }
}


document.getElementById("initial_solution").addEventListener("click", function(event) {
    event.preventDefault();
    gerarGrafoBL();
});

gerarGrafoBL = async () => {
  try {
    const minValue = document.getElementById("minValue").value;
    const maxValue = document.getElementById("maxValue").value;
    const response = await fetch(URL + "/gera_grafo_bl", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({"numeroDeNos": 30, "minValue": minValue, "maxValue": maxValue})
    });

    // Converte a resposta em JSON
    const data = await response.json();

    // Mostra no console
    console.log("Resposta do servidor:", data);
   
    // Limpa o container e adiciona a nova imagem
    const container = document.getElementById("graphContainer");
    container.innerHTML = "";
    container.appendChild(img);

  } catch (error) {
    console.error("Erro ao gerar o grafo:", error);
  }
};

document.getElementById("resetButton").addEventListener("click", function(event) {
    event.preventDefault();
    gerarRelatorio();
});
gerarRelatorio = async () => {
    let data;
    try {
      const response = await fetch(URL + "/gerar_relatorio", {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });
        data = await response.json();
        console.log("Relatório recebido:", data);
  
    } catch (error) {
      console.error("Erro ao gerar o relatório:", error);
    }

      tableRelatorio =  document.getElementById("relatorioTable");
    //faça os dados da tabela aqui
    tableRelatorio.innerHTML = ""; // Limpa a tabela antes de adicionar novos dados

    // Adiciona o cabeçalho da tabela
    const header = tableRelatorio.createTHead();
    const headerRow = header.insertRow(0);
    const headers = ["Método", "Ganho Total (%)", "Número de Execuções","Tamanho da População", "Configurações"];
    headers.forEach((text, index) => {
        const cell = headerRow.insertCell(index);
        cell.innerText = text;
    });
  const tfoot = tableRelatorio.createTFoot();


let footers = [];

Object.keys(data).forEach(metodo => {
    const ganhos = data[metodo].ganho_total || [];
    const execucoes = data[metodo].num_execucoes || [];
    const configs = data[metodo].configuracoes || [];
    const tamanhosPopulacao = data[metodo].tamanho_populacao || [];

    const max = Math.max(
        ganhos.length,
        execucoes.length,
        configs.length,
        tamanhosPopulacao.length
    );

    for (let i = 0; i < max; i++) {
        const row = tableRelatorio.insertRow();

        row.insertCell(0).innerText = metodo;
        row.insertCell(1).innerText = ganhos[i] !== undefined ? Number(ganhos[i]).toFixed(2) : "-";
        row.insertCell(2).innerText = execucoes[i] !== undefined ? execucoes[i] : "-";
        row.insertCell(3).innerText = tamanhosPopulacao[i] !== undefined ? tamanhosPopulacao[i] : "-";
        row.insertCell(4).innerText = configs[i] !== undefined ? JSON.stringify(configs[i]) : "-";
    }

    
    let media = "-";
    if (ganhos.length > 0) {
        const soma = ganhos.reduce((a, b) => a + b, 0);
        media = (soma / ganhos.length).toFixed(2);
    }

   
    footers.push({
        metodo: metodo,
        media: media
    });
});


footers.forEach(f => {
    const footerRow = tfoot.insertRow();
    footerRow.insertCell(0).innerText = `${f.metodo} - Média dos Ganhos (%)`;
    footerRow.insertCell(1).innerText = f.media;
    footerRow.insertCell(2).innerText = "-";
    footerRow.insertCell(3).innerText = "-";
    footerRow.insertCell(4).innerText = "-";
});
}



document.getElementById("searchForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
     data.limite = data.limite ? parseInt(data.limite, 10) : undefined;
     data.initial_temp = data.initial_temp ? parseFloat(data.initial_temp) : undefined;
     data.final_temp = data.final_temp ? parseFloat(data.final_temp) : undefined;
     data.cooling_rate = data.cooling_rate ? parseFloat(data.cooling_rate) : undefined;
    console.log("Enviando JSON:", data);

    const response = await fetch(URL + "/calcular-rota-bl", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log("Resposta do servidor:", result);
    
   // Aqui você pode adicionar a lógica para lidar com o resultado da busca
   if (result.resultado) {
       document.getElementById("caminho").innerText = "Caminho: " + result.resultado.sf + " Custo total: " + result.resultado.vf + " Solucão inicial: " + result.resultado.si + " Custo inicial: " + result.resultado.vi;
    ;

// Define limite de tamanho para a imagem
img.style.maxWidth = "100%";
img.style.height = "auto";
img.style.display = "block";
img.style.margin = "0 auto";

// Adiciona a imagem ao container
resultContainer.appendChild(img);
   } else {
       document.getElementById("caminho").innerText = "Erro ao calcular a rota.";
   }
});
