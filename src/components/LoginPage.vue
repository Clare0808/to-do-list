<template>
 <div class="login">
    <transition name="slide" mode="out-in">
        <div class="sign-in" v-if="signIn" key="sign-in">
            <div class="title">Sign In</div>
            <div class="input-flame">
                <div class="input-title">E-mail</div>
                <input class="input"
                    placehoder="Please enter your e-mail ..."
                    v-model.trim="mail"/>
            </div>
            <div class="input-flame">
                <div class="input-title">Password</div>
                <input class="input"
                    placehoder="Please enter your password ..."
                    v-model.trim="password"/>
            </div>
            <div class="button">
                <div class="sign-in-btn">Sign In</div>
                <div class="sign-up-btn" @click="toggleSignUp">Sign Up</div>
            </div>
        </div>
    </transition>
    <transition name="slide" mode="out-in">
        <div class="sign-up" v-if="signUp" key="sign-up">
            <div class="title">Sign Up</div>
            <div class="input-flame">
                <div class="input-title">Name</div>
                <input class="input"
                    placehoder="Please enter your name ..."
                    v-model.trim="username"/>
            </div>
            <div class="input-flame">
                <div class="input-title">E-mail</div>
                <input class="input"
                    placehoder="Please enter your e-mail ..."
                    v-model.trim="mail"/>
            </div>
            <div class="input-flame">
                <div class="input-title">Password</div>
                <input class="input"
                    placehoder="Please enter your password ..."
                    v-model.trim="password"/>
            </div>
            <div class="input-flame">
                <div class="input-title">Confirm Password</div>
                <input class="input"
                    placehoder="Please enter your password again ..."
                    v-model.trim="conPassword"/>
            </div>
            <div class="button">
                <div class="sign-in-btn" @click="Sendinfo">Sign Up</div>
                <div class="sign-up-btn" @click="toggleSignIn">Sign In</div>
            </div>
        </div>
    </transition>
 </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'LoginPage',
  setup () {
    const signIn = ref(false)
    const signUp = ref(false)
    const mail = ref('')
    const username = ref('')
    const password = ref('')
    const conPassword = ref('')

    const toggleSignIn = () => {
      signIn.value = true
      signUp.value = false
    }

    const toggleSignUp = () => {
      signIn.value = false
      signUp.value = true
    }

    const Sendinfo = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/signup', { // 向後端發送請求
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username: username.value, mail: mail.value, password: password.value }) // 將任務內容轉換為 JSON 格式
        })

        if (!response.ok) {
          throw new Error('Network response was not ok')
        }

        console.log('新增使用者資訊成功:', await response.json())
      } catch (error) {
        console.error('新增使用者資訊失敗:', error)
      }

      // 清空輸入框
      username.value = ''
      mail.value = ''
      password.value = ''
      conPassword.value = ''
    }

    onMounted(() => {
      signIn.value = true
    })

    return {
      signIn,
      signUp,
      username,
      mail,
      password,
      conPassword,
      toggleSignIn,
      toggleSignUp,
      Sendinfo
    }
  }
}
</script>

<style scoped>
.login{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 100vw;
    height: 100vh;
    position: relative;
    overflow-y: hidden;
}
.title{
  width: 340px;
  font-size: 30px;
  font-weight: bold;
  color: #46A3FF;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #CECEFF;
}
.sign-in {
    background-color: #FFFFFF;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0px 0px 5px 3px #ceceff;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: absolute;
    transition: transform 0.6s ease, opacity 0.6s ease;
}
.input-flame {
    margin: 20px;
    display: flex;
    flex-direction: column;
}
.input-title {
    text-align: start;
}
.input {
    width: 300px;
    height: 30px;
    border: 2px solid #ACD6FF;
    border-radius: 12px;
    margin-right: 10px;
}
.input:focus{
    border: 2px solid #46A3FF;
    outline: none;
}
.button {
    display: flex;
    justify-content: center;
    align-items: center;
}
.sign-in-btn {
    width: 100px;
    height: 40px;
    background-color: #46A3FF;
    color: #FFFFFF;
    border-radius: 22px;
    line-height: 40px;
    text-align: center;
    margin: 10px;
}
.sign-in-btn:hover{
  background-color: #ACD6FF;
  color: #46A3FF;
}
.sign-up-btn {
    width: 100px;
    height: 40px;
    background-color: #CECEFF;
    color: #FFFFFF;
    border-radius: 22px;
    line-height: 40px;
    text-align: center;
    margin: 10px;
}
.sign-up-btn:hover{
  background-color: #ACD6FF;
  color: #46A3FF;
}
.sign-up {
    background-color: #FFFFFF;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0px 0px 5px 3px #ceceff;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: absolute;
    transition: transform 0.6s ease, opacity 0.6s ease;
}

.slide-enter-active, .slide-leave-active {
  transition: all 1s ease;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(100%);
}
.slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.slide-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}
</style>
