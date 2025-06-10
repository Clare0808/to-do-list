<template>
  <div class="home">
    <div class="title">Welcome!</div>
    <div class="sec-title">Let's create your to-do list.</div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home{
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  width: 100vw;
  height: 100vh;
}
.title{
  font-size: 60px;
  color: #005AB5;
  margin: 20px;
}
.sec-title{
  font-size: 25px;
  color: #46A3FF;
}
</style>
