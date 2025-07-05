<template>
  <div>
    <canvas ref="ganttChartCanvas" style="width: 100vw;"></canvas>
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
    const gannttLabel = ref([])
    const gannttTime = ref([])

    const Gettaskinfo = async () => {
      const response = await fetch('http://localhost:5000/api/list/history')
      const data = await response.json()

      const filtered = data.tasks.filter(task => task.user_id === userMail.value)

      const formatDate = (gmtStr) => {
        const d = new Date(gmtStr)
        const yyyy = d.getFullYear()
        const mm = String(d.getMonth() + 1).padStart(2, '0')
        const dd = String(d.getDate()).padStart(2, '0')
        return `${yyyy}-${mm}-${dd}`
      }

      gannttLabel.value = filtered.map(task => task.task)
      gannttTime.value = filtered.map(task => {
        const startDate = formatDate(task.task_time_start)
        const endDate = formatDate(task.task_time_end)
        return [startDate, endDate]
      })
    }

    onMounted(async () => {
      await Gettaskinfo()
      await nextTick()

      const ctx = ganttChartCanvas.value.getContext('2d')

      chart.value = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: gannttLabel.value,
          datasets: [
            {
              label: '專案週期',
              backgroundColor: ['rgba(255, 26, 104, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)'],
              borderColor: ['rgba(255, 26, 104, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)'],
              // 長條圖的粗度
              barPercentage: 0.4,
              data: gannttTime.value
            }
          ]
        },
        options: {
          // 這個很重要要設定這個長條圖才會變成橫的
          indexAxis: 'y',
          responsive: true,
          scales: {
            x: {
              // 開始的日期
              min: '2025-07-01',
              type: 'time',
              time: {
                unit: 'day'
              }
            },
            y: {
              beginAtZero: true
            }
          }
        }
      })
    })

    return {
      ganttChartCanvas,
      chart,
      gannttLabel,
      userMail,
      Gettaskinfo
    }
  }
}
</script>
