let getHeatMapData = country => {
    return new Promise((res, rej) => {
        $.ajax({
            url: `/heatMap?country=${country}`,
            success: response => {
                let data = [{
                    z: JSON.parse(response),
                    x: ['danceability', 'energy', 'speechiness', 'valence', 'tempo', 'acousticness', 'duration_ms', 'loudness', 'key'],
                    y: ['danceability', 'energy', 'speechiness', 'valence', 'tempo', 'acousticness', 'duration_ms', 'loudness', 'key'],
                    type: 'heatmap',
                    hoverongaps: false
                }]
                res(data);
            }
        });
    });
}


getHeatMapData('spain').then(res => {
    let layout = {
        width: 1000,
        height: 600,
        paper_bgcolor: 'rgba(0, 0, 0, 0)',
        plot_bgcolor: 'rgba(0, 0, 0, 0)',
        font: {
            color: 'white'
        }
    }
    Plotly.newPlot('heatmap', res, layout)
})

$('#heat-select').change(function() {
    getHeatMapData(this.value).then(res => { Plotly.newPlot('heatmap', res, layout) })
})



/*
$.ajax({
    url: '/relation?country=spain&x=energy&y=acousticness',
    success: res => {
        res = JSON.parse(res)
        var data = [
            {
                x: res.x,
                y: res.y,
                type: 'scatter',
                mode: 'markers'
            }
          ];
          Plotly.newPlot('relation', data);
    }
})
*/

let getTopMinData = country => {
    return new Promise((res, rej) => {
        $.ajax({
            url: `/topmin?country=${country}`,
            success: response => {
                response = JSON.parse(response)
                let data = [
                    {
                        x: ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40-45', '45-50'],
                        y: response.y,
                        type: 'bar'
                    }
                ]
                res(data)
            }
        })
    })
}


getTopMinData('spain').then(res => {
    let layout = {
        paper_bgcolor: 'rgba(0, 0, 0, 0)',
        plot_bgcolor: 'rgba(0, 0, 0, 0)',
        font: {
            color: 'white'
        }
    }
    Plotly.newPlot('top-min', res, layout)
    getTopMinData('germany').then(res => { Plotly.addTraces('top-min', res) })
    getTopMinData('finland').then(res => { Plotly.addTraces('top-min', res) })
    getTopMinData('turkey').then(res => { Plotly.addTraces('top-min', res) })

})


let drawPie = (country, plotId) => {
    $.ajax({
        url: `/pie?country=${country}`,
        success: res => {
            res = JSON.parse(res)
            var data = [
                {
                    values: res.values,
                    labels: res.labels,
                    type: 'pie',
                }
              ];
              let layout = {
                paper_bgcolor: 'rgba(0, 0, 0, 0)',
                plot_bgcolor: 'rgba(0, 0, 0, 0)',
                font: {
                    color: 'white'
                }
            }
              Plotly.newPlot(plotId, data, layout);
        }
    })
}

drawPie('spain', 'pie-es')
drawPie('germany', 'pie-de')
drawPie('turkey', 'pie-tk')
drawPie('finland', 'pie-fn')


let getKeys = country => {
    return new Promise((res, rej) => {
        $.ajax({
            url: `/keys?country=${country}`,
            success: response => {
                response = JSON.parse(response)
                let data = [
                    {
                        x: response.x,
                        y: response.y,
                        type: 'bar',
                    }
                  ];
                  res(data)
            }
        })
    });
}


getKeys('spain').then(res => {
    let layout = {
        paper_bgcolor: 'rgba(0, 0, 0, 0)',
        plot_bgcolor: 'rgba(0, 0, 0, 0)',
        font: {
            color: 'white'
        }
    }
    Plotly.newPlot('keys', res, layout)
    getKeys('germany').then(res => { Plotly.addTraces('keys', res) })
    getKeys('finland').then(res => { Plotly.addTraces('keys', res) })
    getKeys('turkey').then(res => { Plotly.addTraces('keys', res) })
})