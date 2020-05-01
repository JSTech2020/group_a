<template>
    <div class="container">
        <h1 class="header">Story Similarity</h1>
        <div id="similarity-search"
             class="form-inline justify-content-center">
            <input class="form-control"
                   v-model="size"/>
            <button class="btn bg-primary"
                    @click="updateHeatMap()">
                Find
            </button>
            &nbsp;&nbsp;
            <button class="btn bg-primary2"
                    @click="exportPNG()">
                Export
            </button>
        </div>

        <div id="heat-map-container">
            <plotly :data="plotlyData"
                    :layout="plotlyLayout"
                    id="plotly-heatmap"
                    :display-mode-bar="false">
            </plotly>

        </div>

        <p>The most similar stories are {{ mostSim[0]}} and {{ mostSim[1] }} with similarity value {{ mostSim[2] }}</p>
        <p>The least similar stories are {{ leastSim[0] }} and {{ leastSim[1] }} with similarity value {{ leastSim[2]
            }}</p>
    </div>
</template>

<script>
    import axios from "axios";
    import * as svg from 'save-svg-as-png';
    import {Plotly} from 'vue-plotly'

    export default {
        name: "Similarity",
        components: {
            "plotly": Plotly,
        },
        data() {
            return {
                size: 10,
                sims: [],
                ids: {},
                mostSimilar: {},
                leastSimilar: {},
                mostSim: ["0", "0", 0.0],
                leastSim: ["0", "0", 0.0],
                plotlyData: [],
                plotlyLayout: {}
            };
        },
        async created() {
            await this.updateHeatMap()
        },

        methods: {
            async updateHeatMap() {
                await this.getSimilarities();
                await this.populateHeatMap();
            },
            getSimilarities() {
                const path = 'http://localhost:5000/get_heatmap_data?size=' + this.size;
                return axios.get(path)
                    .then((res) => {
                        this.ids = res.data.ids;
                        this.sims = res.data.result;
                        this.mostSimilar = JSON.parse(res.data.mostSimilar);
                        this.leastSimilar = JSON.parse(res.data.leastSimilar);
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });
            },

            populateHeatMap() {
                let xValues = this.ids;
                let yValues = this.ids;
                let zValues = this.sims;

                let colorScaleValue = [
                    [0, '#85BBD7'],
                    [1, '#086688']
                ];

                let annotations = [];
                for (let i = 0; i++; xValues.length) {
                    for (let j = 0; j++; j < i) {
                        let temp = {
                            x: i,
                            y: j,
                            font: {color: 'black'},
                            text: zValues[i][j],
                            xref: 'x',
                            yref: 'y',
                            showarrow: false

                        }
                        annotations.push(temp)
                    }
                }


                // Populate data for heatmat
                this.plotlyData = [{
                    x: xValues,
                    y: yValues,
                    z: zValues,
                    type: 'heatmap',
                    colorscale: colorScaleValue,
                    showscale: false
                }];

                // Edit Layout for heatmap
                this.plotlyLayout = {
                    title: 'Similarity Heatmap',
                    annotations: annotations,
                    xaxis: {
                        ticks: '',
                        side: 'bottom'
                    },
                    yaxis: {
                        ticks: '',
                        ticksuffix: ' ',
                        width: 700,
                        height: 700,
                        autosize: false
                    }
                };

                // update most similar and least similar stories
                let pair, similarity;

                // mostSim
                pair = this.mostSimilar["pair"];
                similarity = this.mostSimilar["similarity"];
                pair = pair[Object.keys(pair)[0]];
                similarity = similarity[Object.keys(similarity)[0]];
                this.mostSim[0] = pair[0];
                this.mostSim[1] = pair[1];
                this.mostSim[2] = similarity.toFixed(2);

                // leastSim
                pair = this.leastSimilar["pair"];
                similarity = this.leastSimilar["similarity"];
                pair = pair[Object.keys(pair)[0]];
                similarity = similarity[Object.keys(similarity)[0]];
                this.leastSim[0] = pair[0];
                this.leastSim[1] = pair[1];
                this.leastSim[2] = similarity.toFixed(2);
            },
            exportPNG() {
                let element = document.getElementById("plotly-heatmap").querySelector("svg");
                let scale = 10
                let filename = "similarity_heatmap_" + Date.now() + ".png"
                svg.saveSvgAsPng(
                    element,
                    filename,
                    {scale: scale}
                );
            },


            async drawHeatMap() {


                // let margin = {top: 30, right: 30, bottom: 30, left: 30},
                //     width = 1000 - margin.left - margin.right,
                //     height = 1000 - margin.top - margin.bottom;
                //
                // // append the svg object to the body of the page
                // let svg = d3.select("#heat-map-container")
                //     .append("svg")
                //     .attr("width", width + margin.left + margin.right)
                //     .attr("height", height + margin.top + margin.bottom)
                //     .append("g")
                //     .attr("transform",
                //         "translate(" + margin.left + "," + margin.top + ")");
                //
                // let myGroups = this.ids;
                // let myVars = this.ids;
                // let myData = this.sims;
                //
                // // Build X scales and axis:
                // var x = d3.scaleBand()
                //     .range([0, width])
                //     .domain(myGroups)
                //     .padding(0.01);
                // svg.append("g")
                //     .attr("transform", "translate(0," + height + ")")
                //     .call(d3.axisBottom(x))
                //
                // // Build X scales and axis:
                // var y = d3.scaleBand()
                //     .range([height, 0])
                //     .domain(myVars)
                //     .padding(0.01);
                // svg.append("g")
                //     .call(d3.axisLeft(y));
                //
                // // Build color scale
                // var myColor = d3.scaleLinear()
                //     .range(["white", "#69b3a2"])
                //     .domain([1, 100])
                // alert(myData)
                // svg.selectAll()
                //     .data(myData, function (d) {
                //         return d.group + ':' + d.variable;
                //     })
                //     .enter()
                //     .append("rect")
                //     .attr("x", function (d) {
                //         return x(d.group)
                //     })
                //     .attr("y", function (d) {
                //         return y(d.variable)
                //     })
                //     .attr("width", x.bandwidth())
                //     .attr("height", y.bandwidth())
                //     .style("fill", function (d) {
                //         return myColor(d.value)
                //     })
                //

            }
        },

    }
</script>

<style scoped>
    #similarity-search{
        margin-top: 10px;
        padding-left: 20px;
    }
    .btn{
        margin-left: 2px;
        margin-right: 2px;
    }
</style>