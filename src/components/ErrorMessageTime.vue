<template>
 <div class="error-message-time">Please choose time !</div>
</template>

<script>
export default {
  name: 'ErrorMessageTime'
}
</script>

<style scoped>
.error-message-time {
  color: #FF5151;
  font-size: 20px;
  text-align: center;
  margin-top: 20px;
}

@media (max-width: 1200px) {
  .error-message-time {
    margin-top: 0;
    margin-bottom: 20px;
  }
}
</style>
