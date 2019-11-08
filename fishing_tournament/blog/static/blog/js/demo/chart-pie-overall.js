// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var chart_pie_overall = document.getElementById("chart-pie-overall");

$.ajax({
    method:'GET',
    url: '/data_barcharts/',
    success:function(data_barcharts){
        console.log(data_barcharts);
        var myPieChart = new Chart(chart_pie_overall, {
            type: 'doughnut',
            data: {
              labels: data_barcharts.label_data,
              datasets: [{
                data: data_barcharts.overall_data,
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#fd7e14', '#f6c23e', '#e74a3b', '#36b9cc', '#6610f2', '#e83e8c', '#20c9a6', '#36b9cc;'],
                hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#d16002', '#d1990a', '#b12316', '#237e8b', '#4309a2', '#ac145a', '#15826c', '#20717d'],
                hoverBorderColor: "rgba(234, 236, 244, 1)",
              }],
            },
            options: {
              maintainAspectRatio: false,
              tooltips: {
                mode:'label',
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
                callbacks: {
                    label: function(tooltipItem, data) { 
                        var indice = tooltipItem.index;                 
                        return data.labels[indice] +' : '+data.datasets[0].data[indice] + 'cm';
                    }
                }
              },
              legend: {
                display: true
              },
              cutoutPercentage: 10,
            },
          });
    },
    error:function(data){
        console.error();
    }
})