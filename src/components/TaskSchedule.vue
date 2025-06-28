<template>
 <div class="schedule">
    <transition-group name="fade">
      <div class="calendar" v-if="show">
        <div class="month-title">
          <i class="fa-solid fa-arrow-left" @click="Changemonth(-1)"></i>
          <div class="month">{{ currentmonth }}</div>
          <i class="fa-solid fa-arrow-right" @click="Changemonth(1)"></i>
        </div>
        <div class="day-flame">
            <div class="week"
              v-for="(w, index) in weeks"
              :key="index"
            >{{w}}</div>
            <div class="day"
                v-for="(i, index) in monthalldays"
                :key="index"
                @click.stop="Clickday(index)"
                :class="{
                  active: index === currentclick,
                  markRad: showmarkred[(todaymonth + 1) + ' / ' + i],
                  markGreen: showmarkgreen[(todaymonth + 1) + ' / ' + i] && !showmarkred[(todaymonth + 1) + ' / ' + i]
                }"
            >{{ i }}
            </div>
        </div>
      </div>
      <div class="work-flame" v-if="show">
        <div class="task-date" v-if="outputday !== ''">{{ outputday }}</div>
        <div class="non-task-date" v-if="outputday === ''">Please choose date.</div>
        <transition-group name="task" tag="div" class="task-flame">
          <div class="non-task" v-if="tasks.length === 0">Nothing here.</div>
          <div
            class="task"
            v-for="(t, index) in tasks"
            :key="t.task_id || index"
            :class="{
              'done-tasks': t.task_type,
              'not-done-tasks': !t.task_type
            }"
          >{{ t.task }}</div>
        </transition-group>
      </div>
    </transition-group>
</div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { userMail } from '@/components/LoginPage.vue'

export default {
  name: 'Schedule',
  setup () {
    const dayclick = ref(false)
    const currentclick = ref('')
    const month = ref([
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ])
    const todaymonth = ref(0)
    const currentmonth = ref('')
    const weeks = ref([
      'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'
    ])
    const lastdayweek = ref(6)
    const days = ref([
      31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ])
    const currentday = ref(0)
    const monthalldays = ref([])
    const remainderdays = ref(0)
    const chosenday = ref('')
    const outputday = ref('')
    const showmarkred = ref({})
    const showmarkgreen = ref({})
    const tasks = ref([])
    const show = ref(false)

    // 點擊日期
    const Clickday = (index) => {
      currentclick.value = index
      dayclick.value = !dayclick.value

      chosenday.value = index - remainderdays.value + 1 // 將索引轉換為實際日期

      outputday.value = (todaymonth.value + 1) + ' / ' + chosenday.value // 格式化輸出日期

      Gettask() // 獲取當前選擇日期的任務
    }

    // 取得當前月份
    const Getmonth = () => {
      todaymonth.value = new Date().getMonth()
      currentmonth.value = month.value[todaymonth.value]
      currentday.value = days.value[todaymonth.value]

      remainderdays.value = 6 - lastdayweek.value // 計算剩餘天數
    }

    // 創建當月的所有天數
    const Createdays = () => {
      monthalldays.value = [] // 清空當月所有天數

      remainderdays.value = 6 - lastdayweek.value

      remainderdays.value = (7 - remainderdays.value) % 7 // 更新剩餘天數並確保為 7 的倍數

      // 填充上個月的空白天數
      for (let i = 1; i <= remainderdays.value; i++) {
        monthalldays.value.push(' ')
      }

      for (let i = 1; i <= currentday.value; i++) {
        monthalldays.value.push(i)

        lastdayweek.value = (lastdayweek.value + 1) % 7 // 更新最後一天的星期數
      }
    }

    // 切換月份
    const Changemonth = (num) => {
      if (num < 0) {
        todaymonth.value = (todaymonth.value - 1 + 12) % 12 // 確保月份在 0 ~ 12 間
      } else {
        todaymonth.value = (todaymonth.value + 1 + 12) % 12
      }

      currentmonth.value = month.value[todaymonth.value]
      currentday.value = days.value[todaymonth.value]

      currentclick.value = '' // 重置當前點擊的日期

      Createdays()
    }

    // 獲取任務時間
    /* const Gettasktime = async () => {
      let time = (todaymonth.value + 1) + ' / ' + chosenday.value
      if (currentclick.value === '' || chosenday.value === '') {
        time = ''
      }

      try {
        const response = await fetch('http://localhost:5000/api/list/time', { // 向後端發送請求
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ time: time }) // 將任務內容轉換為 JSON 格式
        })

        if (!response.ok) {
          throw new Error('Network response was not ok')
        }

        const result = await response.json()
        console.log('成功新增任務時間', result)
      } catch (error) {
        console.error('新增任務時間失敗:', error)
      }
    } */

    // 創建標記
    const CreateMark = async () => {
      const response = await fetch('http://localhost:5000/api/list/history')

      const { tasks } = await response.json() // 從後端獲取任務數據
      showmarkred.value = {} // 初始化紅色標記對象
      showmarkgreen.value = {} // 初始化綠色標記對象

      for (const task of tasks) {
        if (task.user_id === userMail.value && !task.task_type) {
          const time = task.task_time_end
          showmarkred.value[time] = true // 根據任務時間設置標記
        } else if (task.user_id === userMail.value && task.task_type) {
          const time = task.task_time_end
          showmarkgreen.value[time] = true
        }
      }
    }

    // 獲取任務
    const Gettask = async () => {
      const response = await fetch('http://localhost:5000/api/list/history')
      const data = await response.json()

      tasks.value = data.tasks.filter(task => task.user_id === userMail.value && task.task_time_end === outputday.value)
    }

    onMounted(() => {
      show.value = true // 顯示日曆組件

      Getmonth() // 初始化當前月份

      Createdays() // 創建當月的所有天數

      CreateMark() // 創建標記

      Gettask() // 獲取任務
    })

    return {
      dayclick,
      currentclick,
      month,
      todaymonth,
      currentmonth,
      weeks,
      lastdayweek,
      days,
      currentday,
      monthalldays,
      remainderdays,
      chosenday,
      outputday,
      showmarkred,
      showmarkgreen,
      userMail,
      tasks,
      show,
      Clickday,
      Getmonth,
      Createdays,
      Changemonth,
      // Gettasktime,
      CreateMark,
      Gettask
    }
  }
}
</script>

<style scoped>
.schedule{
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  width: 100vw;
  height: 100vh;
}
.calendar {
  font-size: 20px;
  background-color: #FFFFFF;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0px 0px 5px 3px #ceceff;
}
.month-title {
  display: flex;
  justify-content: space-between;
  border-bottom: 2px solid #CECEFF;
  padding-bottom: 10px;
  margin-bottom: 10px;
}
i {
  color: #005AB5;
  font-size: 16px;
  padding: 10px;
  cursor: pointer;
}
i:hover {
  color: #FFFFFF;
  background-color: #46A3FF;
  border-radius: 20px;
}
.month {
  font-size: 30px;
  font-weight: bold;
  color: #46A3FF;
}
.day-flame {
  display: grid;
  grid-template-columns: repeat(7, 50px);
  gap: 20px;
  justify-content: center;
}
.week {
  color: #005AB5;
  font-size: 20px;
  margin-top: 10px;
}
.day {
  height: 42px;
  color: #005AB5;
  font-size: 20px;
  padding: 2px;
  text-align: center;
  line-height: 42px;
  cursor: pointer;
  border: 1px solid #FFFFFF
}
.day:hover {
  color: #FFFFFF;
  background-color: #46A3FF;
  border-radius: 100%;
  border: 1px solid #46A3FF;
}
.day.active {
  color: #FFFFFF;
  background-color: #46A3FF;
  border-radius: 100%;
  border: 1px solid #46A3FF;
}
.markRad {
  /* color: #FFB5B5;
  font-size: 25px;
  font-weight: bold;
  position: absolute;
  top: 26%;
  right: 43%; */
  border: 1px solid #FFB5B5;
  border-radius: 100%;
}
.markGreen {
  border: 1px solid #A6FFA6;
  border-radius: 100%;
}
.work-flame {
  background-color: #FFFFFF;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0px 0px 5px 3px #ceceff;
  margin-left: 20px;
  display: flex;
  flex-direction: column;
}
.task-flame {
  max-height: 350px;
  overflow-y: auto;
  flex: 1;
}
.task-date {
  width: 340px;
  font-size: 30px;
  font-weight: bold;
  color: #46A3FF;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #CECEFF;
}
.non-task-date {
  width: 340px;
  font-size: 30px;
  font-weight: bold;
  color: #CECEFF;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #CECEFF;
}
.non-task{
  color: #CECEFF;
  font-size: 20px;
  font-weight: bold;
  margin-top: 10px;
}
.task{
  width: 300px;
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
  position: relative;
  z-index: 0;
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

.fade-enter-active, .fade-leave-active {
  transition: all 1s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.task-enter-active, .task-leave-active {
  transition: opacity 1s;
}
.task-enter-from, .task-leave-to {
  opacity: 0;
}
.task-enter-to, .task-leave-from {
  opacity: 1;
}
</style>
