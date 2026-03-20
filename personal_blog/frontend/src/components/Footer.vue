<template>
  <!--
    页脚组件
    显示网站版权信息和链接
  -->
  <footer class="footer">
    <div class="footer-container">
      <!-- 版权信息 -->
      <div class="copyright">
        <p>&copy; {{ currentYear }} 个人博客. All rights reserved.</p>
      </div>
      
      <!-- 技术栈说明 -->
      <div class="tech-stack">
        <span>Powered by</span>
        <el-tag size="small" type="info">Django</el-tag>
        <el-tag size="small" type="success">Vue 3</el-tag>
        <el-tag size="small" type="warning">Element Plus</el-tag>
      </div>
    </div>
  </footer>
</template>

<script setup>
/**
 * 页脚组件
 * 
 * 功能：
 * - 显示版权信息
 * - 显示技术栈标签
 */
import { computed } from 'vue'

// 计算当前年份
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  background-color: #fff;
  border-top: 1px solid #e4e7ed;
  padding: 20px 0;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.copyright {
  color: #909399;
  font-size: 14px;
}

.tech-stack {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 14px;
}

.tech-stack span {
  margin-right: 4px;
}
</style>
