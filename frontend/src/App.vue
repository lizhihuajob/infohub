/**
 * 根组件
 */
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
// 根组件不需要额外逻辑
</script>

<style>
#app {
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>
