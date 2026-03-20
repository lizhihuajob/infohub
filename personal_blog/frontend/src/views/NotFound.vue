<template>
  <!--
    404 页面
    当访问不存在的页面时显示
  -->
  <div class="not-found-page">
    <el-result
      icon="warning"
      title="404"
      sub-title="抱歉，您访问的页面不存在"
    >
      <template #extra>
        <router-link to="/">
          <el-button type="primary">返回首页</el-button>
        </router-link>
      </template>
    </el-result>
  </div>
</template>

<script setup>
/**
 * 404 页面组件
 * 
 * 功能：
 * - 显示友好的 404 错误信息
 * - 提供返回首页的链接
 */
</script>

<style scoped>
.not-found-page {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
