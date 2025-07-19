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
import { logOut } from '@/components/LoginPage.vue'

export default {
  name: 'HomeView',
  setup () {
    const show = ref(false)
    const router = useRouter()

    const ChangePage = () => {
      if (logOut.value) {
        router.push('/login') // 如果用戶未登錄，則重定向到登錄頁面
      } else {
        router.push('/list') // 如果用戶已登錄，則重定向到列表頁面
      }
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
  justify-content: center;
  align-items: center;
  text-align: center;
  width: 100vw;
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
