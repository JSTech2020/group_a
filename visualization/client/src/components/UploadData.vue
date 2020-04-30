<template>
    <div class="container">
        <h1 class="header">Upload Data</h1>
        <p>Please Upload the file having file-type ".csv" (Make sure the fields are separated by ";" character)</p>

        <div class="form-inline">
            <label>
                <input type="file"
                       id="file"
                       ref="file"
                       accept=".csv"
                       v-on:change="handleFileUpload()"/>
            </label>

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
                let formData = new FormData();
                formData.append('file', this.file);
                const path = 'http://localhost:5000/upload_data';
                let self = this;
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
</script>

<style scoped>

</style>