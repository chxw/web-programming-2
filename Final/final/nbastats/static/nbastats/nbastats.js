document.addEventListener('DOMContentLoaded', function () {

    clickAveragesGraphed();

});

function clickAveragesGraphed() {
    let button = document.querySelector('.graphed');

    button.onclick = displayGraph;
}

function displayGraph() {

    fetchSeasonAverages();

    async function fetchSeasonAverages() {
        const response = await fetch("https://data.nba.net/data/10s/prod/v1/2020/players/2544_profile.json");
        const season_Averages = await response.json();

        const regSeason = season_Averages.league.standard.stats.regularSeason.season;

        let data = [];
        let parseTime = d3.timeParse("%Y");

        console.log(regSeason);

        regSeason.forEach(function (season) {
            // Get stats
            let datapt = season.total; 
            // Add year attribute 
            datapt.year = parseTime(season.seasonYear);
            // Add to data list
            data.push(datapt);
        });

        let bio = document.querySelector('.bio');
        bio.style.display = 'none';

        let graph = document.querySelector('.graph');
        graph.style.display = 'block';

        // set the dimensions and margins of the graph
        let margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

        let svg = d3.select('.graph')
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

        // Add X axis --> it is a date format
        const x = d3.scaleTime()
            .domain(d3.extent(data, function(d) { return d.year; }))
            .range([ 0, width ]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
        
        // Add Y axis
        const y = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return +d.apg; })])
            .range([ height, 0 ]);
        svg.append("g")
            .call(d3.axisLeft(y));

        // Add the line
        svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
                .x(function(d) { return x(d.year); })
                .y(function(d) { return y(d.apg); })
            );
    }
}