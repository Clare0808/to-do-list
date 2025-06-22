<template>
  <transition name="fade">
    <div class="home" v-if="show">
      <div class="title">Welcome!</div>
      <div class="sec-title">Let's create your to-do list.</div>
    </div>
  </transition>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'HomeView',
  setup () {
    const show = ref(false)

    onMounted(() => {
      show.value = true
    })

    return {
      show
    }
  }
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

.fade-enter-active, .fade-leave-active {
  transition: all 1s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
