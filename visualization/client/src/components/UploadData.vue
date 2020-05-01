<template>
    <div class="container">
        <h1 class="header">Upload Data</h1>
        <hr>
        <p>Please Upload the file having file-type ".csv" (Make sure the fields are separated by ";" character)</p>


        <div class="form-group files">
            <input type="file"
                   class="form-control"
                   ref="file"
                   accept=".csv"
                   v-on:change="handleFileUpload()"/>
        </div>

        <div class="form-inline">


            <button v-on:click="submitFile()">
                Submit
            </button>
        </div>

    </div>
</template>

<script>
    import axios from "axios";
    export default {
        name: "UploadData",
        data() {
            return {
                file: '',
            };
        },
        methods: {
            handleFileUpload(){
                this.file = this.$refs.file.files[0];
            },
            submitFile() {
                let self = this;
                if(this.file==="" || !this.file){
                    self.$swal({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'No File Uploaded',
                        footer: 'Please upload a file'
                    })
                }
                else if(this.file.type !== "text/csv"){
                    self.$swal({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'File Type Mismatch',
                        footer: 'Please upload a valid .csv file'
                    })
                }else{
                    let formData = new FormData();
                    formData.append('file', this.file);
                    const path = 'http://localhost:5000/upload_data';
                    axios.post( path,
                        formData,
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        }
                    ).then(function(res){
                        if(res.data.status === "success"){
                            self.$swal(
                                'Success!',
                                'Data uploaded successfully',
                                'success'
                            ).then(() => document.location.href="/" )

                        }

                    })
                        .catch(function(e){
                            console.log(e);
                        });
                }

            }
        }
    }
</script>

<style scoped>
    .files input {
        outline: 2px dashed #92b0b3;
        outline-offset: -10px;
        -webkit-transition: outline-offset .15s ease-in-out, background-color .15s linear;
        transition: outline-offset .15s ease-in-out, background-color .15s linear;
        padding: 120px 0px 85px 35%;
        text-align: center !important;
        margin: 0;
        width: 100% !important;
    }
    .files input:focus{     outline: 2px dashed #92b0b3;  outline-offset: -10px;
        -webkit-transition: outline-offset .15s ease-in-out, background-color .15s linear;
        transition: outline-offset .15s ease-in-out, background-color .15s linear; border:1px solid #92b0b3;
    }
    .files{ position:relative}
    .files:after {  pointer-events: none;
        position: absolute;
        top: 60px;
        left: 0;
        width: 50px;
        right: 0;
        height: 56px;
        content: "";
        background-image: url(https://image.flaticon.com/icons/png/128/109/109612.png);
        display: block;
        margin: 0 auto;
        background-size: 100%;
        background-repeat: no-repeat;
    }
    .color input{ background-color:#f1f1f1;}
    .files:before {
        position: absolute;
        bottom: 10px;
        left: 0;  pointer-events: none;
        width: 100%;
        right: 0;
        height: 57px;
        display: block;
        margin: 0 auto;
        color: #2ea591;
        font-weight: 600;
        text-transform: capitalize;
        text-align: center;
    }
</style>