<template>
 <div class="error-message">Please enter tasks !</div>
</template>

<script>
export default {
  name: 'ErrorMessage'
}
</script>

<style scoped>
.error-message {
  color: #FF5151;
  font-size: 20px;
  text-align: center;
  margin-top: 20px;
}

@media (max-width: 1200px) {
  .error-message {
    margin-top: 0;
    margin-bottom: 20px;
  }
}
</style>
