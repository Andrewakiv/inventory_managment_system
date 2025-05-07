document.addEventListener("DOMContentLoaded", function () {
    const yearSelect = document.getElementById("year");
    const filterForm = document.getElementById("filterForm");
    const materialId = document.getElementById("chartContainer").dataset.materialId;
  
    $.ajax({
      url: "/inventory/filter-options/",
      type: "GET",
      dataType: "json",
      success: (jsonResponse) => {
        jsonResponse.options.forEach(option => {
          yearSelect.append(new Option(option, option));
        });
        loadAllCharts(yearSelect.options[0].value, materialId);
      },
      error: () => console.log("Failed to fetch chart filter options!")
    });
  
    filterForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const year = yearSelect.value;
      loadAllCharts(year, materialId);
    });
  });
  
  function loadChart(chart, endpoint) {
    $.ajax({
      url: endpoint,
      type: "GET",
      dataType: "json",
      success: (jsonResponse) => {
        const title = jsonResponse.title;
        const labels = jsonResponse.data.labels;
        const datasets = jsonResponse.data.datasets;
  
        chart.data.datasets = [];
        chart.data.labels = [];
  
        chart.options.title.text = title;
        chart.options.title.display = true;
        chart.data.labels = labels;
        datasets.forEach(dataset => {
          chart.data.datasets.push(dataset);
        });
        chart.update();
      },
      error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
    });
  }
  
  function loadAllCharts(year, materialId) {
    loadChart(salesChart, `/inventory/sales/${year}/${materialId}/`);
  }
  
  let salesCtx = document.getElementById("salesChart").getContext("2d");
  let salesChart = new Chart(salesCtx, {
    type: "bar",
    options: {
      responsive: true,
      title: {
        display: false,
        text: ""
      }
    }
  });
  