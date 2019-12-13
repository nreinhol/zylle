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
                data: data_barcharts.sum_of_each_division,
                backgroundColor: ['#F29F05', '#9F5B33', '#623C73', '#386E58', '#D95204', '#735725', '#82718A', '#97BAAC', '#59331D', '#BF903D', '#A65F37', '#A1426C', '#FF711F'],
                hoverBackgroundColor: ['#9c6603', '#4b2b18', '#3e2649', '#274c3d', '#923703', '#4d3a19', '#504655', '#649782', '#27160d', '#8e6b2d', '#764427', '#793151', '#b84300'],
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
                        return data.labels[indice] +' : '+data.datasets[0].data[indice] + ' cm';
                    }
                }
              },
              legend: {
                display: true
              },
              cutoutPercentage: 15,
            },
          });
    },
    error:function(data){
        console.error();
    }
})