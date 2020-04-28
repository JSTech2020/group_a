<template>
    <div class="container">
        {{sims}}<br>

        <div id="heat-map-container">

        </div>
    </div>
</template>

<script>
    import axios from "axios";
    import * as d3 from "d3";

    export default {
        name: "Similarity",
        data() {
            return {
                sims: {},
                ids:{},
                mostSimilar: {},
                leastSimilar: {}
            };
        },
        async created() {
            await this.getSimilarities();
            await this.drawHeatMap();
        },

        methods: {
            getSimilarities() {
                const path = 'http://localhost:5000/similarities';
                return axios.get(path)
                    .then((res) => {
                        this.ids = res.data.ids;
                        this.sims = JSON.parse(res.data.result);
                        this.mostSimilar = res.data.mostSimilar;
                        this.leastSimilar = res.data.leastSimilar;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });
            },
            async drawHeatMap() {

                let margin = {top: 30, right: 30, bottom: 30, left: 30},
                    width = 1000 - margin.left - margin.right,
                    height = 1000 - margin.top - margin.bottom;

                // append the svg object to the body of the page
                let svg = d3.select("#heat-map-container")
                    .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform",
                        "translate(" + margin.left + "," + margin.top + ")");

                let myGroups = this.ids;
                let myVars = this.ids;
                let myData = this.sims;

                // Build X scales and axis:
                var x = d3.scaleBand()
                    .range([0, width])
                    .domain(myGroups)
                    .padding(0.01);
                svg.append("g")
                    .attr("transform", "translate(0," + height + ")")
                    .call(d3.axisBottom(x))

                // Build X scales and axis:
                var y = d3.scaleBand()
                    .range([height, 0])
                    .domain(myVars)
                    .padding(0.01);
                svg.append("g")
                    .call(d3.axisLeft(y));

                // Build color scale
                var myColor = d3.scaleLinear()
                    .range(["white", "#69b3a2"])
                    .domain([1, 100])
                alert(myData)
                svg.selectAll()
                    .data(myData, function (d) {
                        alert(d)
                        return d.group + ':' + d.variable;
                    })
                    .enter()
                    .append("rect")
                    .attr("x", function (d) {
                        return x(d.group)
                    })
                    .attr("y", function (d) {
                        return y(d.variable)
                    })
                    .attr("width", x.bandwidth())
                    .attr("height", y.bandwidth())
                    .style("fill", function (d) {
                        return myColor(d.value)
                    })


            }
        },

    }
</script>

<style scoped>

</style>