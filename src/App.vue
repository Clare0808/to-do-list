<template>
  <div class="flame">
    <nav>
      <div class="user">
        <i class="fa-solid fa-user" id="user"></i>
        <div class="user-name">User</div>
      </div>
      <router-link to="/">Home</router-link>
      <router-link to="/list">List</router-link>
      <router-link to="/status">Status</router-link>
      <i class="fa-solid fa-arrow-right-from-bracket" id="log-out"></i>
    </nav>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  /*background-image: url('./assets/background.jpg');
  background-size: contain;
  background-repeat: no-repeat;*/
  background-image: linear-gradient(to top, #FFFFFF 0%, #ACD6FF 100%);
  height: 100vh;
}

/* 刪除頁面四周的空白處 */
body{
  margin: 0;
  padding: 0;
}

.flame{
  display: flex;
  justify-content: center;
  align-items: center;
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
</style>
