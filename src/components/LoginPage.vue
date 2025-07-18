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
                    v-model.trim="password"
                    type="password"/>
            </div>
            <div class="button">
                <div class="sign-in-btn" @click="LoginInfo">Sign In</div>
                <div class="sign-up-btn" @click="Togglesignup">Sign Up</div>
            </div>
            <div class="error" v-show="error">{{ errormsg }}</div>
            <div class="success" v-show="success">{{ successmsg }}</div>
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
                    v-model.trim="password"
                    type="password"/>
            </div>
            <div class="input-flame">
                <div class="input-title">Confirm Password</div>
                <input class="input"
                    placehoder="Please enter your password again ..."
                    v-model.trim="conPassword"
                    type="password"/>
            </div>
            <div class="button">
                <div class="sign-in-btn" @click="Sendinfo">Sign Up</div>
                <div class="sign-up-btn" @click="Togglesignin">Sign In</div>
            </div>
            <div class="error" v-show="error">{{ errormsg }}</div>
            <div class="success" v-show="success">{{ successmsg }}</div>
        </div>
    </transition>
 </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export const userMail = ref('')
export const userName = ref('')
export const showNav = ref(false)
export const logOut = ref(true)

export default {
  name: 'LoginPage',
  setup () {
    const signIn = ref(false)
    const signUp = ref(false)
    const mail = ref('')
    const username = ref('')
    const password = ref('')
    const conPassword = ref('')
    const error = ref(false)
    const errormsg = ref('')
    const success = ref(false)
    const successmsg = ref('')
    const router = useRouter()

    // 切換到登入頁面
    const Togglesignin = () => {
      signIn.value = true
      signUp.value = false

      error.value = false // 清除錯誤訊息
      success.value = false // 清除成功訊息

      CleanInputFlame() // 清空輸入框
    }

    // 切換到註冊頁面
    const Togglesignup = () => {
      signIn.value = false
      signUp.value = true

      error.value = false // 清除錯誤訊息
      success.value = false // 清除成功訊息

      CleanInputFlame() // 清空輸入框
    }

    // 發送使用者資訊到後端
    const Sendinfo = async () => {
      AssureSignUpInputFlame() // 確認輸入框是否有填寫內容

      await AssureEmailDiff() // 檢查郵箱是否已存在

      if (!error.value) {
        if (password.value !== conPassword.value) { // 檢查密碼是否一致
          error.value = true
          errormsg.value = 'Password does not match !'
        } else {
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

          CleanInputFlame() // 清空輸入框

          error.value = false // 清除錯誤訊息

          success.value = true // 顯示成功訊息
          successmsg.value = 'Sign up successfully !' // 設置成功訊息

          setTimeout(() => {
            Togglesignin()
          }, 1000) // 1秒後切換到登入頁面
        }
      }
    }

    // 登入使用者資訊
    const LoginInfo = async () => {
      AssureSignInInputFlame() // 確認輸入框是否有填寫內容

      if (!error.value) {
        const response = await fetch('http://localhost:5000/api/login')
        const data = await response.json()

        const user = data.data.find(user => user.mail === mail.value) // 查找使用者郵箱

        if (user) {
          if (user.password.trim() === password.value.trim()) {
            userMail.value = user.mail // 設置全局使用者郵箱
            userName.value = user.username // 設置全局使用者名稱
            localStorage.setItem('userMail', userMail.value) // 將使用者郵箱存入 localStorage
            localStorage.setItem('userName', userName.value) // 將使用者名稱存入 localStorage

            // 清空輸入框
            mail.value = ''
            password.value = ''

            error.value = false // 清除錯誤訊息

            success.value = true // 顯示成功訊息
            successmsg.value = 'Login successfully !' // 設置成功訊息

            setTimeout(() => {
              router.push('/')
              showNav.value = true // 顯示導航欄
              logOut.value = false // 更改登出狀態
            }, 1000) // 1秒後跳轉到首頁
          } else {
            error.value = true
            errormsg.value = 'Incorrect password !'
          }
        } else {
          error.value = true
          errormsg.value = 'User not found !'
        }
      }
    }

    // 檢查郵箱是否已存在
    const AssureEmailDiff = async () => {
      const response = await fetch('http://localhost:5000/api/login')
      const data = await response.json()

      const userMail = data.data.map(user => user.mail) // 獲取所有使用者郵箱

      if (userMail.includes(mail.value)) { // 檢查郵箱是否已存在
        error.value = true
        errormsg.value = 'This e-mail is already registered !'
      }
    }

    // 檢查登入輸入框是否有填寫內容
    const AssureSignUpInputFlame = () => {
      if (username.value === '') {
        error.value = true
        errormsg.value = 'Please enter your name !'
      } else if (mail.value === '') {
        error.value = true
        errormsg.value = 'Please enter your e-mail !'
      } else if (password.value === '') {
        error.value = true
        errormsg.value = 'Please enter your password !'
      } else if (conPassword.value === '') {
        error.value = true
        errormsg.value = 'Please enter your password again !'
      } else {
        error.value = false
      }
    }

    // 檢查註冊輸入框是否有填寫內容
    const AssureSignInInputFlame = () => {
      if (mail.value === '') {
        error.value = true
        errormsg.value = 'Please enter your e-mail !'
      } else if (password.value === '') {
        error.value = true
        errormsg.value = 'Please enter your password !'
      } else {
        error.value = false
      }
    }

    // 清空登入輸入框
    const CleanInputFlame = () => {
      mail.value = ''
      username.value = ''
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
      error,
      errormsg,
      success,
      successmsg,
      Togglesignin,
      Togglesignup,
      Sendinfo,
      LoginInfo,
      AssureSignInInputFlame,
      AssureSignUpInputFlame,
      AssureEmailDiff,
      CleanInputFlame
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
    cursor: pointer;
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
  cursor: pointer;
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
.error {
  position: absolute;
  bottom: 10px;
  color: #FF5151;
  font-size: 20px;
  text-align: center;
}
.success {
  position: absolute;
  bottom: 10px;
  color: #46A3FF;
  font-size: 20px;
  text-align: center;
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

@media (max-width: 510px) {
  .title {
    width: 280px;
  }
  .input {
    width: 230px;
  }
}
</style>
