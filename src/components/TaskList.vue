<template>
  <div class="list">
    <div class="add-tasks-flame">
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
        <div class="tasks-flame">
          <div class="non-tasks" v-if="allTasks.length === 0">Nothing here.</div>
          <div class="task"
            @click="Taskclick(index)"
            :class="{active : clicked.includes(index)}"
            v-for="(t, index) in allTasks"
            :key="index"
            >
            <hr v-show="clicked.includes(index)"/>
            {{ t.task }}
            <span class="delete-btn" @click.stop="Deletetask(index)">x</span>
          </div>
        </div>
      </div>
      <ErrorMessage v-show="nontask"/>
    </div>
    <div class="filter-flame">
      <div class="filter">
        <div class="filter-title">Done !</div>
        <div class="non-tasks" v-if="finishedTasks.length === 0">Nothing here.</div>
        <div class="filter-tasks-flame">
          <div class="done-tasks" v-for="(t, index) in finishedTasks" :key="index">{{ t.task }}</div>
        </div>
      </div>
      <div class="filter">
        <div class="filter-title">Not Done !</div>
        <div class="non-tasks" v-if="notFinishedTasks.length === 0">Nothing here.</div>
        <div class="filter-tasks-flame">
         <div class="not-done-tasks" v-for="(t, index) in notFinishedTasks" :key="index">{{ t.task }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
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
    const finishedTasks = ref([])
    const notFinishedTasks = ref([])

    // 點擊任務時切換樣式
    const Taskclick = (index) => {
      if (clicked.value.includes(index)) {
        clicked.value = clicked.value.filter(i => i !== index) // 移除已點擊的任務索引
        finishedTasks.value = finishedTasks.value.filter(t => t !== allTasks.value[index]) // 從已完成任務中移除該任務
        notFinishedTasks.value.push(allTasks.value[index]) // 將該任務添加到未完成任務列表
      } else {
        clicked.value.push(index) // 添加新的點擊任務索引
        finishedTasks.value.push(allTasks.value[index]) // 將點擊的任務添加到已完成任務列表
        notFinishedTasks.value = notFinishedTasks.value.filter(t => t !== allTasks.value[index])
      }
    }

    // 新增任務
    const Addtask = async () => {
      if (task.value.trim() === '') {
        nontask.value = true // 顯示錯誤訊息
      } else {
        try {
          const response = await fetch('http://localhost:5000/api/list', { // 向後端發送請求
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: task.value, task_type: false }) // 將任務內容轉換為 JSON 格式
          })

          if (!response.ok) {
            throw new Error('Network response was not ok')
          }

          const result = await response.json()
          console.log('成功新增任務', result)

          await Gettasks()

          task.value = '' // 清空輸入框
          nontask.value = false // 隱藏錯誤訊息
        } catch (error) {
          console.error('新增任務失敗:', error)
        }
      }
    }

    // 刪除任務
    const Deletetask = async (index) => {
      const taskToDelete = allTasks.value[index]
      const taskId = taskToDelete.task_id

      const response = await fetch('http://localhost:5000/api/list/delete', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ taskId })
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      await Gettasks()

      /* const taskToDelete = allTasks.value[index] // 獲取要刪除的任務

      allTasks.value.splice(index, 1) // 從任務列表中刪除指定索引的任務

      // 更新 clicked
      clicked.value = clicked.value
        .filter(i => i !== index) // 移除當前刪除的 index
        .map(i => i > index ? i - 1 : i) // 後面所有 index 減 1，避免錯位

      const removeTask = (arr) => {
        const idx = arr.indexOf(taskToDelete) // 查找要刪除的任務在列表中的索引
        if (idx !== -1) arr.splice(idx, 1) // 刪除該任務
      }

      removeTask(finishedTasks.value) // 從已完成任務列表中刪除該任務
      removeTask(notFinishedTasks.value) // 從未完成任務列表中刪除該任務 */
    }

    // 取得紀錄
    const Gettasks = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/list/history')
        const history = await response.json()

        allTasks.value = history.tasks.filter(task => task.task.trim() !== '')
      } catch (error) {
        console.error('獲取任務失敗:', error)
      }
    }

    onMounted(() => {
      Gettasks() // 在組件掛載時獲取任務資料
    })

    return {
      clicked,
      task,
      nontask,
      allTasks,
      finishedTasks,
      notFinishedTasks,
      Taskclick,
      Addtask,
      Deletetask,
      Gettasks
    }
  }
}
</script>

<style scoped>
.list{
  display: flex;
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
.add-tasks-flame{
  display: flex;
  flex-direction: column;
}
.work-flame{
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #FFFFFF;
  padding: 30px;
  border-radius: 12px;
}
.input-flame{
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
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
.tasks-flame{
  max-height: 300px;
  overflow-y: auto;
  flex: 1;
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
.filter{
  background-color: #FFFFFF;
  width: 300px;
  padding: 30px;
  border-radius: 12px;
  margin: 20px;
  margin-left: 40px;
  text-align: center;
}
.filter-title{
  color: #46A3FF;
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 30px;
  padding-bottom: 10px;
  border-bottom: 2px solid #CECEFF;
}
.non-tasks{
  color: #CECEFF;
  font-size: 20px;
  font-weight: bold;
}
.filter-tasks-flame{
  /* 增加滾動軸 */
  max-height: 150px;
  overflow-y: auto;
  flex: 1;
}
.done-tasks{
  height: 30px;
  color: #02DF82;
  background-color: #DFFFDF;
  font-size: 20px;
  border-radius: 12px;
  text-align: center;
  padding: 5px;
  padding-left: 20px;
  line-height: 30px;
  margin: 10px;
}
.not-done-tasks{
  height: 30px;
  color: #FF5151;
  background-color: #FFB5B5;
  font-size: 20px;
  border-radius: 12px;
  text-align: center;
  padding: 5px;
  padding-left: 20px;
  line-height: 30px;
  margin: 10px;
}
</style>
