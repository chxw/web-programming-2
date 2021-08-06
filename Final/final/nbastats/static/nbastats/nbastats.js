document.addEventListener('DOMContentLoaded', function () {

    clickElement('#graph-link', displayGraph);
    clickElement('#bio-link', displayBio);
    clickElement('.favorite', favoritePlayer);

});

function getpropName(obj, value) {
    for (let key in obj) {
        if (obj[key] == value) {
            return key;
        }
    }
    return false;
}

function clickElement(element, onClickFunction) {
    let button = document.querySelector(element);

    if (button) {
        button.onclick = onClickFunction;
    }
}

function favoritePlayer() {
    currentURL = window.location.href;
    index = currentURL.split('/player/')[0];
    playerId = currentURL.split('/player/')[1];

    // Check whether user wants to favorite (favorite = true) or unfavorite (favorite = false)
    let favorite = false;
    if (this.innerText == "Favorite") {
        favorite = true;
    }

    fetch(index + "/bookmark", {
        method: 'PUT',
        body: JSON.stringify({
            playerId: playerId,
            favorite: favorite
        })
    })
        .then(response => console.log(response))
        .then(() => {
            if (favorite) {
                this.innerText = "Unfavorite";
            } else {
                this.innerText = "Favorite";
            }
            clickElement('.favorite', favoritePlayer);
        });
}

function displayBio() {
    let graphLink = document.querySelector('#graph-link');
    graphLink.classList.remove("active");

    this.classList.add("active");

    let bio = document.querySelector('.bio');
    bio.style.display = 'block';

    let graphDiv = document.querySelector('.graph-div');
    graphDiv.style.display = 'none';
}

async function displayGraph() {

    currentURL = window.location.href;
    playerId = currentURL.split('/player/')[1];

    await createGraph(playerId, this);

    // Switch tabs in HTML
    let bioLink = document.querySelector('#bio-link');
    bioLink.classList.remove("active");

    this.classList.add("active");

    let bio = document.querySelector('.bio');
    bio.style.display = 'none';

    let graphDiv = document.querySelector('.graph-div');
    graphDiv.style.display = 'block';

    async function createGraph(playerId) {
        // Fetch data
        const response = await fetch("https://data.nba.net/data/10s/prod/v1/2020/players/" + String(playerId) + "_profile.json");
        const season_Averages = await response.json();

        const regSeason = season_Averages.league.standard.stats.regularSeason.season;

        let data = [];
        let parseTime = d3.timeParse("%Y");
        regSeason.forEach(function (season) {
            // Get season totals
            let datapt = season.total;
            // Add year attribute 
            datapt.year = parseTime(season.seasonYear);
            data.push(datapt);
        });

        // Set dimensions and margins of the graph
        let margin = { top: 10, right: 100, bottom: 30, left: 30 },
            width = 460 - margin.left - margin.right,
            height = 400 - margin.top - margin.bottom;

        // Append the svg object to the body of the page
        let svg = d3.select(".graph")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

        // Group options
        let attributes = Object.keys(data[0]);

        // Add options to the button
        d3.select("#selectButton")
            .selectAll('myOptions')
            .data(attributes)
            .enter()
            .append('option')
            .text(function (d) { return d; }) // text showed in the menu
            .attr("value", function (d) { return d; }); // corresponding value returned by the button

        // A color scale: one color for each group
        let myColor = d3.scaleOrdinal()
            .domain(attributes)
            .range(d3.schemeSet2);

        // Add X axis
        let x = d3.scaleTime()
            .domain(d3.extent(data, function (d) { return d.year; }))
            .range([0, width]);
        svg.append("g")
            .attr("class", "x axis")
            .text("Year")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        // Add Y axis
        let y = d3.scaleLinear()
            .domain([0, d3.max(data, function (d) { return +d.ppg; })])
            .range([height, 0]);
        svg.append("g")
            .attr("class", "y axis")
            .text("PPG")
            .call(d3.axisLeft(y));

        // Initialize line with 
        let line = svg
            .append('g')
            .append("path")
            .datum(data)
            .attr("d", d3.line()
                .x(function (d) { return x(+d.year); })
                .y(function (d) { return y(+d.ppg); })
            )
            .attr("stroke", function (d) { return myColor(d.ppg); })
            .style("stroke-width", 4)
            .style("fill", "none");

        // A function that updates the chart
        function update(selectedGroup) {

            // Create new data with selection
            var dataFilter = data.map(function (d) { return { year: d.year, value: d[selectedGroup] }; });

            // Update X axis
            let x = d3.scaleTime()
                .domain(d3.extent(data, function (d) { return d.year; }))
                .range([0, width]);
            svg.selectAll("g.x.axis")
                .text("Year")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x));

            // Update Y axis
            let y = d3.scaleLinear()
                .domain([0, d3.max(data, function (d) { return +d[selectedGroup]; })])
                .range([height, 0]);
            svg.selectAll("g.y.axis")
                .text(getpropName(data, function (d) { return +d[selectedGroup]; }))
                .call(d3.axisLeft(y));

            // Use new data to draw line
            line
                .datum(dataFilter)
                .transition()
                .duration(1000)
                .attr("d", d3.line()
                    .x(function (d) { return x(+d.year); })
                    .y(function (d) { return y(+d.value); })
                )
                .attr("stroke", function (d) { return myColor(selectedGroup); });
        }

        // When the button is changed, run the updatefunction
        d3.select("#selectButton").on("change", function (d) {
            var selectedOption = d3.select(this).property("value");
            update(selectedOption);
        });
    }
}