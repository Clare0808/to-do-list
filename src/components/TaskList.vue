<template>
  <div class="list">
    <div class="add-tasks-flame">
      <transition name="slide">
        <div class="work-flame" v-if="showworkflame">
          <div class="title">To-Do List</div>
          <div class="input-flame">
            <input class="input"
              placehoder="Please enter your tasks ..."
              v-model.trim="task"
              @keydown.enter="Addtask"
            />
            <i class="fa-regular fa-calendar"
                id="calendar-btn"
                @click="Togglecalendar"
                :class="{active: calendarclick}"
            ></i>
            <div class="add-btn" @click.stop="Addtask">Add</div>
          </div>
          <div class="tasks-flame" ref="scrollalltasksbox">
            <Calendar v-show="calendarclick" id="calendar" @selectTime="Handletime"/>
            <div class="non-tasks" v-if="allTasks.length === 0">Nothing here.</div>
            <transition-group name="fade">
              <div class="task"
                @click="Taskclick(index)"
                :class="{active : clicked.includes(t.task_id)}"
                v-for="(t, index) in allTasks"
                :key="index"
              >
                <hr v-show="clicked.includes(t.task_id)"/>
                  {{ t.task }}
                  <span class="time">{{ t.task_time }}</span>
                  <span class="delete-btn" @click.stop="Deletetask(index)">x</span>
              </div>
              </transition-group>
          </div>
        </div>
      </transition>
      <div class="message" v-show="addmsg">Task added successfully!</div>
      <ErrorMessage v-show="nontask"/>
      <ErrorMessageTime v-show="nontime"/>
    </div>
    <transition name="slide">
      <div class="filter-flame" v-if="showworkflame">
        <div class="filter">
          <div class="filter-title">Done !</div>
          <div class="non-tasks" v-if="finishedTasks.length === 0">Nothing here.</div>
          <div class="filter-tasks-flame" ref="scrolldonetasksbox">
            <transition-group name="fade">
              <div class="done-tasks"
                v-for="t in finishedTasks"
                :key="t.task_id + '-done'"
                :ref="el => donetaskrefs[t.task_id] = el"
              >{{ t.task }}</div>
            </transition-group>
          </div>
        </div>
        <div class="filter">
          <div class="filter-title">Undo !</div>
          <div class="non-tasks" v-if="notFinishedTasks.length === 0">Nothing here.</div>
          <div class="filter-tasks-flame" ref="scrollundotasksbox">
            <transition-group name="fade">
              <div class="not-done-tasks"
                v-for="t in notFinishedTasks"
                :key="t.task_id + '-undo'"
                :ref="el => undotaskrefs[t.task_id] = el"
              >{{ t.task }}</div>
            </transition-group>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, reactive } from 'vue'
import ErrorMessage from '@/components/ErrorMessage.vue'
import ErrorMessageTime from '@/components/ErrorMessageTime.vue'
import Calendar from '@/components/Calendar.vue'

export default {
  name: 'TaskList',
  components: {
    ErrorMessage,
    ErrorMessageTime,
    Calendar
  },
  setup () {
    const clicked = ref([])
    const task = ref('')
    const nontask = ref(false)
    const nontime = ref(false)
    const addmsg = ref(false)
    const allTasks = ref([])
    const finishedTasks = ref([])
    const notFinishedTasks = ref([])
    const calendarclick = ref(false)
    const time = ref('')
    const scrollalltasksbox = ref(null)
    const scrollundotasksbox = ref(null)
    const donetaskrefs = reactive({})
    const undotaskrefs = reactive({})
    const showworkflame = ref(false)

    const Togglecalendar = async () => {
      time.value = '' // 清空時間選擇

      calendarclick.value = !calendarclick.value
    }

    // 點擊任務時切換樣式
    const Taskclick = async (index) => {
      const taskId = allTasks.value[index].task_id
      const taskType = clicked.value.includes(taskId)

      // 向後端發送請求更新任務狀態
      try {
        const response = await fetch('http://localhost:5000/api/list/update', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            task_id: taskId,
            task_type: !taskType
          })
        })

        if (!response.ok) {
          throw new Error(`HTTP 錯誤! 狀態碼: ${response.status}`)
        }

        allTasks.value[index].task_type = !taskType // 更新任務狀態

        if (taskType) { // 已完成 變 未完成
          clicked.value = clicked.value.filter(i => i !== taskId)
          finishedTasks.value = finishedTasks.value.filter(task => task.task_id !== taskId)
          notFinishedTasks.value.push(allTasks.value[index])

          await nextTick() // 等待 DOM 更新
          undotaskrefs[taskId]?.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          }) // 將未完成任務滾動到可見區域
        } else { // 未完成 變 已完成
          clicked.value.push(taskId)
          finishedTasks.value = allTasks.value.filter(task => task.task_type)
          notFinishedTasks.value = notFinishedTasks.value.filter(task => task.task_id !== taskId)

          await nextTick() // 等待 DOM 更新
          donetaskrefs[taskId]?.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          }) // 將已完成任務滾動到可見區域
        }
      } catch (error) {
        console.error('任務狀態更新失敗:', error)
      }
    }

    // 新增任務
    const Addtask = async () => {
      // await Gettasktime()

      if (!time.value) {
        console.warn('請先選擇日期')
        nontime.value = true
        return
      }

      if (task.value.trim() === '') {
        nontask.value = true // 顯示錯誤訊息
      } else {
        try {
          const response = await fetch('http://localhost:5000/api/list', { // 向後端發送請求
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: task.value, task_type: false, task_time: time.value }) // 將任務內容轉換為 JSON 格式
          })

          if (!response.ok) {
            throw new Error('Network response was not ok')
          }

          const result = await response.json()
          console.log('成功新增任務', result)

          await Gettasks()

          await nextTick() // 等待 DOM 更新
          Scrollbottomalltasks() // 滾動任務列表到底部
          Scrollbottomundotasks() // 滾動未完成任務列表到底部

          task.value = '' // 清空輸入框
          nontask.value = false // 隱藏錯誤訊息

          time.value = '' // 清空時間選擇
          calendarclick.value = false // 隱藏日曆
          nontime.value = false // 隱藏時間錯誤訊息

          addmsg.value = true // 顯示新增成功訊息

          setTimeout(() => {
            addmsg.value = false
          }, 3000) // 3秒後隱藏新增成功訊息
        } catch (error) {
          console.error('新增任務失敗:', error)
        }
      }
    }

    // 刪除任務
    const Deletetask = async (index) => {
      const taskToDelete = allTasks.value[index]
      const taskId = taskToDelete.task_id

      // 向後端發送請求刪除任務
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

      await Gettasks() // 重新獲取任務列表
    }

    // 取得紀錄
    const Gettasks = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/list/history')
        const history = await response.json()

        allTasks.value = history.tasks.filter(task => task.task.trim() !== '')
        finishedTasks.value = allTasks.value.filter(task => task.task_type)
        notFinishedTasks.value = allTasks.value.filter(task => !task.task_type)
      } catch (error) {
        console.error('獲取任務失敗:', error)
      }
    }

    // 獲取任務時間
    const Handletime = (selected) => {
      time.value = selected
      console.log('選擇的日期:', time.value)
    }

    // 滾動任務列表到底部
    const Scrollbottomalltasks = () => {
      nextTick(() => {
        if (scrollalltasksbox.value) {
          scrollalltasksbox.value.scrollTop = scrollalltasksbox.value.scrollHeight
        }
      })
    }

    // 滾動未完成任務列表到底部
    const Scrollbottomundotasks = () => {
      nextTick(() => {
        if (scrollundotasksbox.value) {
          scrollundotasksbox.value.scrollTop = scrollundotasksbox.value.scrollHeight
        }
      })
    }

    onMounted(async () => {
      showworkflame.value = true // 顯示工作區域

      await Gettasks() // 在組件掛載時獲取任務資料

      // 初始化 clicked
      clicked.value = allTasks.value
        .filter(task => task.task_type)
        .map(task => task.task_id)
    })

    return {
      clicked,
      task,
      nontask,
      nontime,
      addmsg,
      allTasks,
      finishedTasks,
      notFinishedTasks,
      calendarclick,
      time,
      scrollalltasksbox,
      donetaskrefs,
      undotaskrefs,
      showworkflame,
      Togglecalendar,
      Taskclick,
      Addtask,
      Deletetask,
      Gettasks,
      Handletime,
      Scrollbottomalltasks
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
  box-shadow: 0px 0px 5px 3px #ceceff;
  position: relative;
  z-index: 1;
}
.input-flame{
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}
.input{
  width: 270px;
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
#calendar-btn {
  font-size: 25px;
  line-height: 35px;
  color: #ACD6FF;
  margin-right: 10px;
  cursor: pointer;
}
#calendar-btn:hover {
  color: #46A3FF;
}
#calendar-btn.active {
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
.time {
  position: absolute;
  right: 60px;
}
.delete-btn{
  position: absolute;
  right: 20px;
}
.message {
  color: #46A3FF;
  font-size: 20px;
  text-align: center;
  margin-top: 20px;
}
.filter{
  background-color: #FFFFFF;
  width: 300px;
  padding: 30px;
  border-radius: 12px;
  margin: 20px;
  margin-left: 40px;
  text-align: center;
  box-shadow: 0px 0px 5px 3px #ceceff;
}
.filter-title{
  color: #46A3FF;
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 30px;
  padding-bottom: 10px;
  border-bottom: 2px solid #CECEFF;
}
#calendar {
  position: absolute;
  z-index: 2;
  top: 150px;
  right: 30px;
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

.slide-enter-active, .slide-leave-active {
  transition: all 1s ease;
}
.slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
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
  transform: translateY(20px);
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
}
</style>
