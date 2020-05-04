<template>
    <div class="container">
        <h1 class="header">Story Similarity</h1>
        <hr>
        <div id="similarity-search"
             class="form-inline justify-content-center">
            <label class="mr-3"
                   for="story-size">
                No. of Stories:
            </label>
            <input class="form-control"
                   id="story-size"
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

        <h3>The most similar stories are
            <a class="btn btn-link pointer-event"
               v-b-modal.story-modal
               href=""
               @click="getStory(getId(mostSim[0]))">
                {{ getTitle2(mostSim[0]) }}
            </a>
            and
            <a class="btn btn-link pointer-event"
               v-b-modal.story-modal
               href=""
               @click="getStory(getId(mostSim[1]))">
                {{ getTitle2(mostSim[1])}}
            </a>
            with similarity value
            {{ mostSim[2] }}
        </h3>
        <h3>The least similar stories are
            <a class="btn btn-link pointer-event"
               v-b-modal.story-modal
               href=""
               @click="getStory(getId(leastSim[0]))">
                {{ getTitle2(leastSim[0])}}
            </a>
            and
            <a class="btn btn-link pointer-event"
               v-b-modal.story-modal
               href=""
               @click="getStory(getId(leastSim[1]))">
                {{ getTitle2(leastSim[1])}}
            </a>
            with similarity value
            {{ leastSim[2]}}
        </h3>
        <br>
        <hr>
        <div class="row">
            <div class="col-sm-10">
                <h1>Stories</h1>
                <hr>

                <table class="table table-hover">
                    <thead>
                    <tr>
                        <th scope="col">S.N.</th>
                        <th scope="col">Story ID</th>
                        <th scope="col">Title</th>
                        <th scope="col">Similar Stories</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="(val,index) in ids_raw" :key="index">
                        <td>{{index}}</td>
                        <td>{{(stories[index])?stories[index].id:""}}</td>
                        <td>{{(stories[index])?stories[index].title:""}}</td>
                        <td>
                            <span v-if="stories[index]">
                                <button type="button"
                                        v-for="(v,i) in stories[index].related_story_id"
                                        v-bind:key="i"
                                        v-bind:title="getTitle(v)"
                                        v-b-modal.story-modal
                                        @click="getStory(v)"
                                        class="btn btn-sm tertiary3">
                                    {{ v }}
                                </button>
                            </span>
                        </td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button"
                                        class="btn bg-secondary btn-sm"
                                        v-b-modal.story-modal
                                        @click="getStory(stories[val].id)">
                                    Detail
                                </button>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <b-modal ref="showStoryDetail"
                 id="story-modal"
                 size="lg"
                 hide-footer
                 v-bind:title="story.title">
            <div class="responsive">
                <table class="table table-striped table-condensed">
                    <tbody>
                    <tr>
                        <td scope="row">Story Id:</td>
                        <td>{{story.id}}</td>
                    </tr>
                    <tr>
                        <td scope="row">Tags:</td>
                        <td>{{listToString(story.tags)}}</td>
                    </tr>
                    <tr>
                        <td scope="row">Related Story Ids:</td>
                        <td>{{listToString(story.related_story_id)}}</td>
                    </tr>
                    <tr>
                        <td scope="row">Abstract:</td>
                        <td>{{story.abstract}}</td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </b-modal>

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
                stories: [],
                similarities: [],
                story: {title:''},
                tags: [],
                size: 10,
                sims: [],
                ids: [],
                ids_raw: [],
                mostSimilar: {},
                leastSimilar: {},
                mostSim: ["0", "0", 0.0],
                leastSim: ["0", "0", 0.0],
                plotlyData: [],
                plotlyLayout: {}
            };
        },
        async created() {
            await this.getStories();
            await this.getSimilarStories();
            await this.updateStories();
            await this.updateHeatMap();
        },

        methods: {
            getStories() {
                const path = 'http://localhost:5000/stories';
                return axios.get(path)
                    .then((res) => {
                        this.stories = res.data.stories;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });
            },
            async getStory(id) {
                const path = 'http://localhost:5000/stories/' + id;
                await axios.get(path)
                    .then((res) => {
                        this.story = res.data.story[0];
                        let temp = this.stories.find(x => x.id === this.story.id)
                        if (temp !== null && temp !== "undefined") {
                            this.story.related_story_id = temp.related_story_id;
                            this.story.tags = temp.tags;
                        }
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });

            },
            getSimilarStories() {
                const path = 'http://localhost:5000/similarities';
                return axios.get(path)
                    .then((res) => {
                        this.similarities = res.data.similarities;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        console.error(error);
                    });
            },
            updateStories() {
                let temp = [];
                for (let i = 0; i < this.stories.length; i++) {
                    temp.push({
                        ...this.stories[i],
                        'related_story_id': this.similarities[i]['related_story_id'],
                        'tags': this.similarities[i]['tags']
                    })
                }
                this.stories = temp;
                return temp;
            },
            async updateHeatMap() {
                await this.getSimilarities();
                await this.populateHeatMap();
            },
            getSimilarities() {
                const path = 'http://localhost:5000/get_heatmap_data?size=' + this.size;
                return axios.get(path)
                    .then((res) => {
                        this.ids_raw = []

                        this.ids = res.data.ids;
                        this.sims = res.data.result;
                        this.mostSimilar = JSON.parse(res.data.mostSimilar);
                        this.leastSimilar = JSON.parse(res.data.leastSimilar);

                        for (let i in this.ids) {
                            let id = this.ids[i]
                            this.ids_raw.push(parseInt((id.split("_"))[1]))
                        }

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

            getTitle(id) {
                let temp = this.stories.find(x => x.id === parseInt(id));
                if (temp !== null && temp !== undefined) {
                    return temp.title;
                } else {
                    return ""
                }
            },

            getTitle2(id) {
                let temp = this.stories.find(x => x.id === parseInt((id.split("_"))[1]));
                if (temp !== null && temp !== undefined) {
                    return temp.title;
                } else {
                    return ""
                }
            },

            getId(id) {
                if (id !== null && id !== "undefined" && id !== "") {
                    return (id.split("_"))[1];
                } else {
                    return "";
                }
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

            },
            listToString(li) {
                if (li !== null && li !== undefined && li !== []) {
                    return li.join(", ");
                } else {
                    return ""
                }
            }
        },

    }
</script>

<style scoped>
    #similarity-search {
        margin-top: 10px;
        padding-left: 20px;
    }

    .btn {
        margin-left: 2px;
        margin-right: 2px;
    }
</style>