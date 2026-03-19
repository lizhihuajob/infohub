<template>
  <!--
    加载动画组件
    用于页面或数据加载时的过渡效果
  -->
  <div class="loading-spinner">
    <el-icon class="spinner-icon" :size="size">
      <Loading />
    </el-icon>
    <p v-if="text" class="loading-text">{{ text }}</p>
  </div>
</template>

<script setup>
/**
 * 加载动画组件
 *
 * Props:
 *   size: 图标大小（默认 40）
 *   text: 加载提示文字（可选）
 */
import { Loading } from '@element-plus/icons-vue'

defineProps({
  size: {
    type: Number,
    default: 40
  },
  text: {
    type: String,
    default: '加载中...'
  }
})
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner-icon {
  animation: spin 1s linear infinite;
  color: #409eff;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  margin-top: 10px;
  color: #909399;
  font-size: 14px;
}
</style>
