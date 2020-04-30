<template>
  <div id="app">
    <nav-bar></nav-bar>
    <router-view/>
  </div>
</template>

<script>
  import Navbar from "./components/Navbar"
  export default {
    name: "App",
    components:{
      "nav-bar":Navbar,
    }
  }
</script>

<style>
  #app{
    /*margin-top: 20px;*/
    font-family: "Helvetica Neue",serif;
  }
  #app h1{
    font-size: 24px;
  }
  #app h2{
    font-size: 18px;
  }
  #app p{
    font-size: 12px;
  }
  #app .bg-primary{
    background: #FDC70F !important;
    color: #323838;
  }
  #app .bg-primary2{
    background: #F38F1F !important;
    color: #323838;
  }
  #app .bg-primary3{
    background: #EC6224 !important;
    color: #323838;
  }
  #app .bg-secondary{
    background: #FEDC6E !important;
    color: #5F696A;
  }
  #app .bg-secondary2{
    background: #F5B063 !important;
    color: #5F696A;
  }
  #app .bg-secondary3 {
    background: #F18A5D !important;
    color: #5F696A;
  }
  #app .tertiary {
    background: #06AED5 !important;
  }
  #app .tertiary2 {
    background: #086688 !important;
  }
  #app .tertiary3 {
    background: #85BBD7 !important;
  }
</style>