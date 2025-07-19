<template>
  <div class="flame">
    <transition-group name="page">
      <nav v-if="showNav">
        <div class="user">
          <router-link to="/login">
            <i class="fa-solid fa-user" id="user"></i>
          </router-link>
          <div class="user-name">{{ userName }}</div>
        </div>
        <router-link to="/">Home</router-link>
        <router-link to="/list">List</router-link>
        <router-link to="/status">Status</router-link>
        <router-link to="/schedule">Schedule</router-link>
        <i class="fa-solid fa-arrow-right-from-bracket" id="log-out" @click="Logout"></i>
      </nav>
    </transition-group>
    <i class="fa-solid fa-bars" id="menu" @click="clickMenu"></i>
    <div class="mobile-menu" v-if="showMenu">
      <router-link to="/" class="page">Home</router-link>
      <router-link to="/list" class="page">List</router-link>
      <router-link to="/status" class="page">Status</router-link>
      <router-link to="/schedule" class="page">Schedule</router-link>
      <div class="page" @click="Logout">Log Out</div>
    </div>
    <router-view/>
  </div>
</template>

<script>
import { userName, userMail, showNav, logOut } from '@/components/LoginPage.vue'
import { useRouter, useRoute } from 'vue-router'
import { onMounted, ref, watch } from 'vue'

export default {
  setup () {
    const router = useRouter()
    const route = useRoute()
    const showMenu = ref(false)

    // 登出功能
    const Logout = () => {
      // 清除本地存儲中的用戶資訊
      localStorage.removeItem('userMail')
      localStorage.removeItem('userName')

      showNav.value = false // 隱藏導航欄
      logOut.value = true // 設置登出狀態

      router.push('/') // 導向登入頁面
    }

    const clickMenu = () => {
      showMenu.value = !showMenu.value // 切換菜單顯示狀態
    }

    watch(route, () => {
      showMenu.value = false // 當路由變化時，隱藏菜單
    })

    onMounted(() => {
      // 檢查本地存儲中的用戶資訊
      const storedMail = localStorage.getItem('userMail')
      const storedName = localStorage.getItem('userName')

      if (storedMail && storedName) {
        // 如果存在，則設置用戶資訊
        userMail.value = storedMail
        userName.value = storedName

        logOut.value = false // 未登出狀態
        showNav.value = true // 顯示導航欄
      } else {
        logOut.value = true
        showNav.value = false
      }
    })

    return {
      userName,
      userMail,
      showNav,
      logOut,
      router,
      route,
      showMenu,
      Logout,
      clickMenu
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  /*background-image: url('./assets/background.jpg');
  background-size: contain;
  background-repeat: no-repeat;*/
  background-image: linear-gradient(to top, #FFFFFF 0%, #ACD6FF 100%);
}

/* 刪除頁面四周的空白處 */
body{
  margin: 0;
  padding: 0;
}

.flame{
  display: flex;
  justify-content: center;
  margin-left: 20px;
}

nav {
  width: 80px;
  height: 85vh;
  background-color: #FFFFFF;
  border-radius: 12px;
  box-shadow: 0px 0px 5px 3px #CECEFF;
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  top: 20px;
}

nav a {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  color: #CECEFF;
  text-decoration: none;  /* 移除文字底線 */
  margin: 10px;
  padding: 10px;
  padding-bottom: 5px;
  transition: transform 0.2s ease-in-out;
}

nav a.router-link-exact-active {
  width: 100%;
  color: #46A3FF;
}

nav a:hover{
  transform: translateY(-3px);
}
.user{
  width: 100px;
  margin-bottom: 50px;
  border-bottom: 2px solid #CECEFF;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
#user{
  width: 40px;
  height: 40px;
  font-size: 38px;
  color: #46A3FF;
  text-align: center;
  border: 3px solid #46A3FF;
  border-radius: 50%;
  cursor: pointer;
}
#user:hover{
  color: #ACD6FF;
  border: 3px solid #ACD6FF;
}
.user-name{
  color: #005AB5;
  text-align: center;
  margin-top: 20px;
}
#log-out{
  color: #CECEFF;
  font-size: 25px;
  position: absolute;
  bottom: 40px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}
#log-out:hover{
  color: #46A3FF;
  transform: translateY(-3px);
}

.page-enter-active, .page-leave-active {
  transition: all 1s ease;
}
.page-enter-from, .page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
.page-enter-to, .page-leave-from {
  opacity: 1;
  transform: translatex(0);
}
#menu {
  display: none;
  font-size: 25px;
  line-height: 50px;
  text-align: center;
  color: #46A3FF;
  background-color: #FFFFFF;
  width: 50px;
  height: 50px;
  border-radius: 25px;
  position: absolute;
  top: 22px;
  left: 20px;
  z-index: 3;
  transition: transform 0.2s ease-in-out;
}
#menu:hover {
  transform: translateY(-3px);
}
.mobile-menu {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #FFFFFF;
  border-radius: 12px;
  border: 2px solid #46A3FF;
  box-shadow: 0px 0px 5px 3px #CECEFF;
  width: 98%;
  height: 250px;
  position: absolute;
  z-index: 2;
}
.page {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  color: #CECEFF;
  text-decoration: none;  /* 移除文字底線 */
  margin: 5px;
  padding: 10px;
  padding-bottom: 5px;
  transition: transform 0.2s ease-in-out;
}
.page:hover {
  transform: translateY(-3px);
}

@media (max-width: 770px) {
  #menu {
    display: block;
  }
  nav {
    display: none;
  }
  .flame {
    margin-left: 0;
  }
}
</style>
