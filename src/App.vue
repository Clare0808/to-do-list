<template>
  <div class="flame">
    <nav>
      <i class="fa-solid fa-user"></i>
      <router-link to="/">Home</router-link>
      <router-link to="/list">List</router-link>
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
  box-shadow: 0px 0px 5px 3px #F0F0F0;
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

nav a {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  color: #005AB5;
  text-decoration: none;  /* 移除文字底線 */
  margin: 10px;
  padding: 10px;
  transition: transform 0.3s ease-in-out;
}

nav a.router-link-exact-active {
  color: white;
  background-color: #ACD6FF;
  border-radius: 20px;
}

nav a:hover{
  color: white;
  background-color: #ACD6FF;
  border-radius: 20px;
  transform: scale(1.2);
}

i{
  width: 40px;
  height: 40px;
  font-size: 38px;
  color: #005AB5;
  text-align: center;
  border: 3px solid #005AB5;
  border-radius: 50%;
  margin-bottom: 50px;
}
</style>
