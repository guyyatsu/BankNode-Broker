    $(document).ready(function () {
        const config = {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: "Price History",
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: [],
                    fill: false,
                }],
            },
            options: {
                responsive: true,
                title: {
                    display: true,
		    // The top title-text is passed by argument.
                    text: document.currentScript.getAttribute("TitleText")
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Value'
                        }
                    }]
                }
            }
        };
                    text: ''
 
        const context = document.getElementById('chart').getContext('2d');

        const lineChart = new Chart(context, config);

        // The data source is passed to the script as an argument.
        const source = new EventSource(document.currentScript.getAttribute("DataSource"));

        source.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (config.data.labels.length === 20) {
                config.data.labels.shift();
                config.data.datasets[0].data.shift();
            }
            config.data.labels.push(data.time);
            config.data.datasets[0].data.push(data.value);
            lineChart.update();
        }
    });
