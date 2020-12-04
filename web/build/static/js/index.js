const buildGraphs = (json) => {
  var counts = {};
  json.forEach(function (x) {
    counts[x.prediction] = (counts[x.prediction] || 0) + 1;
  });
  var ctx = $("#myChart");
  var secondChart = $("#secondChart");
  var thirdChart = $("#thirdChart");
  var data = {
    labels: Object.keys(counts),
    datasets: [
      {
        label: "US's Sizes",
        data: Object.values(counts),
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  new Chart(ctx, {
    type: "bar",
    data: data,
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });

  new Chart(secondChart, {
    data: data,
    type: "doughnut",
  });

  new Chart(thirdChart, {
    data: data,
    type: "polarArea",
  });

  $("#select").change(function () {
    $(".charts").hide();
    $(`#${this.value}`).show();
  });
};

const buildTable = (tableData) => {
  $("#predictionsTable").DataTable({
    columns: [
      { data: "title" },
      { data: "description" },
      {
        data: "prediction",
        render: function (data, type, JsonResultRow, meta) {
          let classes = "box ";
          switch (data) {
            case "S":
              classes += "red";
              break;
            case "M":
              classes += "blue";
              break;
            case "L":
              classes += "yellow";
              break;
          }
          return `<div class="${classes}" style="margin: auto;">${data}</div>`;
        },
      },
    ],
    buttons: ["copy", "csv", "excel", "pdf", "print"],
    order: [0, "desc"],
    data: tableData,
  });
};

$(document).ready(function () {
  $("form").submit(function (evt) {
    evt.preventDefault();
    var formData = new FormData($(this)[0]);
    $.ajax({
      url: "http://localhost:5000/predict",
      type: "POST",
      data: formData,
      async: false,
      cache: false,
      contentType: false,
      enctype: "multipart/form-data",
      processData: false,
      success: function (response) {
        buildTable(response);
        buildGraphs(response);
      },
    });
    return false;
  });
});
