<template>
  <div class="list">
    <div class="work-flame">
      <div class="title">To-Do List</div>
      <div class="input-flame">
        <input class="input"
          placehoder="Please enter your tasks ..."
          v-model.trim="task"
          @keydown.enter="Addtask"
        />
        <div class="add-btn" @click.stop="Addtask">Add</div>
      </div>
      <div class="task"
        @click="Taskclick(index)"
        :class="{active : clicked.includes(index)}"
        v-for="(t, index) in allTasks"
        :key="index"
        >
        <hr v-show="clicked.includes(index)"/>
        {{t}}
        <span class="delete-btn" @click.stop="Deletetask(index)">x</span>
      </div>
    </div>
    <ErrorMessage v-if="nontask"/>
  </div>
</template>

<script>
import { ref } from 'vue'
/* import apiService from '@/services/api' */
import ErrorMessage from '@/components/ErrorMessage.vue'

export default {
  name: 'TaskList',
  components: {
    ErrorMessage
  },
  setup () {
    const clicked = ref([])
    const task = ref('')
    const nontask = ref(false)
    const allTasks = ref([])

    // 點擊任務時切換樣式
    const Taskclick = (index) => {
      if (clicked.value.includes(index)) {
        clicked.value = clicked.value.filter(i => i !== index) // 移除已點擊的任務索引
      } else {
        clicked.value.push(index) // 添加新的點擊任務索引
      }
    }

    // 新增任務
    const Addtask = () => {
      /* const response = apiService.getTasks() */
      if (task.value.trim() === '') {
        nontask.value = true // 顯示錯誤訊息
      } else {
        allTasks.value.push(task.value) // 將輸入的任務添加到任務列表中

        task.value = '' // 清空輸入框

        nontask.value = false // 隱藏錯誤訊息
      }

      /* console.log(response) */
    }

    // 刪除任務
    const Deletetask = (index) => {
      allTasks.value.splice(index, 1) // 從任務列表中刪除指定索引的任務
      clicked.value = clicked.value.filter(i => i !== index) // 移除已刪除任務的索引
    }

    return {
      clicked,
      task,
      nontask,
      allTasks,
      Taskclick,
      Addtask,
      Deletetask
    }
  }
}
</script>

<style scoped>
.list{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  width: 100vw;
  height: 100vh;
}
.title{
  width: 380px;
  font-size: 30px;
  font-weight: bold;
  color: #46A3FF;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #CECEFF;
}
.work-flame{
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #FFFFFF;
  width: 400px;
  padding: 30px;
  border-radius: 12px;
}
.input-flame{
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}
.input{
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
.add-btn{
  width: 60px;
  height: 35px;
  background-color: #46A3FF;
  color: #FFFFFF;
  border-radius: 12px;
  line-height: 35px;
  cursor: pointer;
}
.add-btn:hover{
  background-color: #ACD6FF;
  color: #46A3FF;
}
.task{
  width: 350px;
  height: 30px;
  color: #46A3FF;
  background-color: #ECF5FF;
  font-size: 20px;
  border-radius: 12px;
  text-align: left;
  padding: 5px;
  padding-left: 20px;
  line-height: 30px;
  margin: 5px;
  cursor: pointer;
  position: relative;
  z-index: 0;
}
.task.active{
  color: #CECEFF;
  background-color: #F7FBFF;
}
hr{
  width: 380px;
  border: 1px solid #CECEFF;
  position: absolute;
  top: 26%;
  left: -3px;
  z-index: -1;
}
.delete-btn{
  position: absolute;
  right: 20px;
}
</style>
