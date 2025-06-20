<template>
 <div class="calendar">
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
            :class="{active: index === currentclick}"
        >{{ i }}</div>
    </div>
</div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Calendar',
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

    // 點擊日期
    const Clickday = (index) => {
      currentclick.value = index
      dayclick.value = !dayclick.value

      chosenday.value = index - remainderdays.value + 1 // 將索引轉換為實際日期

      Gettasktime()
    }

    // 取得當前月份
    const Getmonth = () => {
      todaymonth.value = new Date().getMonth()
      currentmonth.value = month.value[todaymonth.value]
      currentday.value = days.value[todaymonth.value]

      remainderdays.value = 6 - lastdayweek.value // 計算剩餘天數
    }

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

      Createdays()
    }

    const Gettasktime = async () => {
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

      currentclick.value = '' // 清除當前點擊的日期
    }

    onMounted(() => {
      Getmonth() // 初始化當前月份

      Createdays() // 創建當月的所有天數
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
      Clickday,
      Getmonth,
      Createdays,
      Changemonth,
      Gettasktime
    }
  }
}
</script>

<style scoped>
.calendar {
  color: #FFFFFF;
  font-size: 20px;
  background-color: #ACD6FF;
  padding: 20px;
  border-radius: 12px;
}
.month-title {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #FFFFFF;
  padding-bottom: 10px;
  margin-bottom: 10px;
}
i {
  font-size: 16px;
  padding: 5px;
  cursor: pointer;
}
i:hover {
  color: #46A3FF;
  background-color: #FFFFFF;
  border-radius: 20px;
}
.month {
  color: #FFFFFF;
  font-size: 20px;
}
.day-flame {
  display: grid;
  grid-template-columns: repeat(7, 30px);
  gap: 5px;
  justify-content: center;
}
.week {
  font-size: 14px;
}
.day {
  font-size: 16px;
  padding: 5px;
  text-align: center;
  cursor: pointer;
}
.day:hover {
  color: #46A3FF;
  background-color: #FFFFFF;
  border-radius: 20px;
}
.day.active {
  color: #46A3FF;
  background-color: #FFFFFF;
  border-radius: 20px;
}
</style>
