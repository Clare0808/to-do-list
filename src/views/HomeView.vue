<template>
  <transition name="fade">
    <div class="home" v-if="show">
      <div class="title">Welcome!</div>
      <div class="sec-title">Let's create your to-do list.</div>
      <div class="start-btn" @click="ChangePage">Start</div>
    </div>
  </transition>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'HomeView',
  setup () {
    const show = ref(false)
    const router = useRouter()

    const ChangePage = () => {
      router.push('/login')
    }

    onMounted(() => {
      show.value = true
    })

    return {
      show,
      router,
      ChangePage
    }
  }
}
</script>

<style scoped>
.home{
  display: flex;
  flex-direction: column;
  align-items: center;
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
.start-btn {
  width: 100px;
  background-color: #46A3FF;
  color: #FFFFFF;
  border-radius: 20px;
  margin-top: 20px;
  padding: 10px;
  cursor: pointer;
}
.start-btn:hover {
  background-color: #ACD6FF;
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
