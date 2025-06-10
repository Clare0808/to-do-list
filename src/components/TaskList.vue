<template>
  <div class="list">
    <div class="title">To-Do List</div>
    <input class="input"/>
  </div>
</template>

<script>
export default {
  name: 'TaskList'
}
</script>

<style scoped>
.list{
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  width: 100vw;
  height: 100vh;
}

</style>
