<template>
  <div class="gantt-chart-flame">
    <div class="title">Gantt Chart</div>
    <div class="flame">
      <div class="gantt-chart-container">
        <canvas ref="ganttChartCanvas" class="chart" width="600" height="300"></canvas>
        <div class="msg" v-if="message">Please select a task.</div>
      </div>
      <div class="chart-info-flame">
        <div class="chart-info">
          <div class="chart-lable"
            v-for="(t, index) in ganttLable"
            :key="index"
            @click="ClickLable(index)"
            :class="{'active': currentIndex === index}"
          >{{ t }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { userMail } from '@/components/LoginPage.vue'
import Chart from 'chart.js/auto'
import 'chartjs-adapter-moment'

export default {
  name: 'GannttChart',
  components: {
  },
  setup () {
    const ganttChartCanvas = ref(null)
    const chart = ref(null)
    const ganttLable = ref([])
    const ganttTime = ref([])
    const ganttType = ref([])
    const currentLable = ref([])
    const currentTime = ref([])
    const currentIndex = ref('')
    const currentType = ref(false)
    const firstDay = ref('')
    const lastDay = ref('')
    const message = ref(true)

    // 獲取任務資訊
    const Gettaskinfo = async () => {
      const response = await fetch('http://localhost:5000/api/list/history')
      const data = await response.json()

      const filtered = data.tasks.filter(task => task.user_id === userMail.value)

      // 格式化日期
      const formatDate = (gmtStr) => {
        const d = new Date(gmtStr)
        const yyyy = d.getFullYear()
        const mm = String(d.getMonth() + 1).padStart(2, '0')
        const dd = String(d.getDate()).padStart(2, '0')
        return `${yyyy}-${mm}-${dd}`
      }

      for (let i = 0; i < filtered.length; i++) {
        for (let j = 0; j < filtered.length - 1; j++) {
          const dateA = new Date(filtered[j].task_time_end)
          const dateB = new Date(filtered[j + 1].task_time_end)

          if (dateA > dateB) {
            const temp = filtered[j]
            filtered[j] = filtered[j + 1]
            filtered[j + 1] = temp
          }
        }
      }

      ganttLable.value = filtered.map(task => task.task)
      ganttTime.value = filtered.map(task => {
        const startDate = formatDate(task.task_time_start)
        const endDate = formatDate(task.task_time_end)
        return [startDate, endDate]
      })
      ganttType.value = filtered.map(task => task.task_type)
    }

    // 獲取當前任務的索引和相關資訊
    const GetCurrentIndex = async (index) => {
      if (chart.value) {
        chart.value.destroy()
        chart.value = null
      }

      currentLable.value = [ganttLable.value[index]]
      currentTime.value = [[
        ganttTime.value[index][0],
        ganttTime.value[index][1]
      ]]
      currentIndex.value = index
      currentType.value = ganttType.value[index]
    }

    // 繪製甘特圖
    const DrawGanttChart = async () => {
      await Gettaskinfo()
      await nextTick() // 確保 DOM 更新完成

      const ctx = ganttChartCanvas.value.getContext('2d') // 獲取 canvas 上下文

      chart.value = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: currentLable.value,
          datasets: [
            {
              label: '專案週期',
              backgroundColor: colors(),
              borderColor: colors(),
              barPercentage: 0.4, // 長條圖的粗度
              data: currentTime.value
            }
          ]
        },
        options: {
          indexAxis: 'y', // 設置為橫向條形圖
          responsive: true, // 使圖表響應式
          maintainAspectRatio: false, // 允許圖表大小隨容器變化
          scales: {
            x: {
              min: firstDay.value, // 開始日期
              max: lastDay.value, // 結束日期
              type: 'time',
              time: {
                unit: 'day'
              }
            },
            y: {
              beginAtZero: true // Y 軸從零開始
            }
          }
        }
      })

      message.value = false // 隱藏提示信息
    }

    // 點擊任務標籤
    const ClickLable = async (index) => {
      await GetCurrentIndex(index)
      await GetFirstDay(index)
      await GetLastDay(index)
      await nextTick()
      await DrawGanttChart()
    }

    // 獲取任務第一天的月份第一天
    const GetFirstDay = (index) => {
      const taskStartDay = ganttTime.value[index][0]
      const date = new Date(taskStartDay)

      firstDay.value = new Date(date.getFullYear(), date.getMonth(), 1)
    }

    // 獲取任務最後一天的月份最後一天
    const GetLastDay = (index) => {
      const taskEndDay = ganttTime.value[index][1]
      const date = new Date(taskEndDay)

      lastDay.value = new Date(date.getFullYear(), date.getMonth() + 1, 0)
    }

    // 根據任務類型返回顏色
    const colors = () => {
      if (currentType.value === true) {
        return '#A6FFA6'
      }
      return '#FFB5B5' // 預設顏色為紅色
    }

    onMounted(async () => {
      await Gettaskinfo()
    })

    return {
      ganttChartCanvas,
      chart,
      ganttLable,
      ganttTime,
      ganttType,
      currentLable,
      currentTime,
      currentIndex,
      currentType,
      firstDay,
      lastDay,
      message,
      colors,
      Gettaskinfo,
      GetCurrentIndex,
      DrawGanttChart,
      ClickLable,
      GetFirstDay,
      GetLastDay
    }
  }
}
</script>

<style scoped>
.gantt-chart-flame {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #FFFFFF;
  padding: 20px;
  border-radius: 12px;
  margin: 10px;
  box-shadow: 0px 0px 5px 3px #ceceff;
}
.title {
  width: 970px;
  font-size: 30px;
  font-weight: bold;
  color: #46A3FF;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #CECEFF;
}
.flame {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.gantt-chart-container {
  height: 200px;
  margin-right: 20px;
  position: relative;
  z-index: 0;
}
.msg {
  color: #CECEFF;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  position: absolute;
  top: 45%;
  right: 40%;
  z-index: 1;
}
.chart {
  width: 650px;
  height: 200px;
}
.chart-info-flame {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 200px;
}
.chart-info {
  max-height: 180px;
  overflow-y: auto;
  flex: 1;
}
.chart-lable {
  width: 200px;
  height: 30px;
  font-size: 20px;
  color: #CECEFF;
  background-color: #F7FBFF;
  border-radius: 12px;
  text-align: left;
  padding: 5px;
  padding-left: 20px;
  line-height: 30px;
  margin: 5px;
  cursor: pointer;
}
.chart-lable.active {
  color: #46A3FF;
  background-color: #ECF5FF;
}
</style>
