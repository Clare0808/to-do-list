<template>
    <div class="status">
      <div class="flame">
        <div class="done-flame">
          <div class="counter">
              <div class="title">Done Tasks</div>
              <div class="done-num">{{ donenum }}</div>
          </div>
          <div class="chart-flame">
            <div class="chart-title">Completion Rate</div>
            <canvas ref="donechart"></canvas>
            <div class="done-rate">{{ donepercentage }}%</div>
          </div>
        </div>
        <div class="undo-flame">
          <div class="counter">
              <div class="title">Undo Tasks</div>
              <div class="undo-num">{{ undonum }}</div>
          </div>
          <div class="chart-flame">
            <div class="chart-title">Incompletion Rate</div>
            <canvas ref="undochart"></canvas>
            <div class="undo-rate">{{ undopercentage }}%</div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables) // 註冊 Chart.js

export default {
  name: 'TaskStatus',
  setup () {
    const donenum = ref('')
    const undonum = ref('')
    const donechart = ref(null)
    const undochart = ref(null)
    const donepercentage = ref(0)
    const undopercentage = ref(0)
    const Donechartpaint = ref(null)
    const Undochartpaint = ref(null)

    const Calculatepercentage = () => {
      const total = donenum.value + undonum.value

      donepercentage.value = Math.round((donenum.value / total) * 100)
      undopercentage.value = Math.round((undonum.value / total) * 100)
    }

    // 獲取任務數量
    const Gettasknumber = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/list/history')
        const data = await response.json()

        donenum.value = data.tasks.filter(task => task.task_type).length
        undonum.value = data.tasks.filter(task => !task.task_type).length

        Calculatepercentage() // 獲取數據後計算百分比
      } catch (error) {
        console.error('獲取任務失敗:', error)
      }
    }

    watch([donepercentage, undopercentage], () => {
      if (Donechartpaint.value) {
        Donechartpaint.value.destroy() // ✅ 先銷毀舊圖表，避免重疊
      }

      // 已完成任務的圖表
      Donechartpaint.value = new Chart(donechart.value, {
        type: 'doughnut', // 設定為甜甜圈圖
        data: {
          labels: ['Done', 'All'], // 設定圖表標籤
          datasets: [{
            data: [donepercentage.value, 100 - donepercentage.value], // 75%已完成
            backgroundColor: ['#A6FFA6', '#F0F0F0'] // 綠色代表完成，灰色代表未完成
          }]
        },
        options: {
          cutout: '70%' // 調整內圈大小
        }
      })

      if (Undochartpaint.value) {
        Undochartpaint.value.destroy() // ✅ 先銷毀舊圖表，避免重疊
      }

      // 未完成任務的圖表
      Undochartpaint.value = new Chart(undochart.value, {
        type: 'doughnut',
        data: {
          labels: ['Undo', 'All'],
          datasets: [{
            data: [undopercentage.value, 100 - undopercentage.value], // 25%未完成
            backgroundColor: ['#FFB5B5', '#F0F0F0'] // 紅色代表完成，灰色代表已完成
          }]
        },
        options: {
          cutout: '70%' // 調整內圈大小
        }
      })
    })

    onMounted(() => {
      Gettasknumber() // 獲取任務數量

      Calculatepercentage() // 計算百分比
    })

    return {
      donenum,
      undonum,
      donechart,
      undochart,
      donepercentage,
      undopercentage,
      Donechartpaint,
      Undochartpaint,
      Calculatepercentage,
      Gettasknumber
    }
  }
}
</script>

<style scoped>
.status {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 100vw;
    height: 100vh;
}
.flame {
    display: flex;
    justify-content: center;
    align-items: center;
}
.done-flame{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.counter {
    width: 300px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 0px 5px 3px #ceceff;
}
.title {
    font-size: 30px;
    font-weight: bold;
    color: #46A3FF;
    padding: 0 20px;
}
.done-num {
    font-size: 40px;
    font-weight: bold;
    color: #02DF82;
    padding: 0 20px;
}
.undo-num {
    font-size: 40px;
    font-weight: bold;
    color: #FF5151;
    padding: 0 20px;
}
.undo-flame {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.chart-flame {
  width: 300px;
  background-color: #FFFFFF;
  padding: 20px;
  border-radius: 12px;
  margin: 20px;
  box-shadow: 0px 0px 5px 3px #ceceff;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}
.chart-title {
  width: 300px;
  font-size: 30px;
  font-weight: bold;
  color: #46A3FF;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #CECEFF;
}
canvas {
  max-width: 200px;
  max-height: 200px;
}
.done-rate {
  font-size: 40px;
  font-weight: bold;
  color: #02DF82;
  position: absolute;
  top: 60%;
  right: 37%;
}
.undo-rate {
  font-size: 40px;
  font-weight: bold;
  color: #FF5151;
  position: absolute;
  top: 60%;
  right: 37%;
}
</style>
