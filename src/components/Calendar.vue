<template>
 <div class="calendar">
    <div class="month">June</div>
    <div class="day-flame">
        <div class="day"
            v-for="(i, index) in 31"
            :key="index"
            @click="Clickday(index)"
            :class="{active: index === currentclick}"
        >{{ i }}</div>
    </div>
</div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Calendar',
  setup () {
    const dayclick = ref(false)
    const currentclick = ref('')
    const calendarclick = ref(false)

    const Togglecalendar = () => {
      calendarclick.value = !calendarclick.value
    }

    const Clickday = (index) => {
      currentclick.value = index
      dayclick.value = !dayclick.value
    }

    return {
      dayclick,
      currentclick,
      calendarclick,
      Togglecalendar,
      Clickday
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
.month {
    color: #FFFFFF;
    font-size: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #FFFFFF;
    margin-bottom: 10px;
}
.day-flame {
    display: grid;
    grid-template-columns: repeat(7, 30px);
    gap: 5px;
    justify-content: center;
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
