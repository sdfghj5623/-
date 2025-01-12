<template>
  <view class="container">
    <text class="large-text">我好懒</text>
  </view>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>

<style scoped>
/* 容器设置为全屏，并居中显示 */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 100% 屏幕高度 */
  width: 100%; /* 100% 屏幕宽度 */
  background-color: #fff;
}

/* 文字样式：使用动态单位使文字占满屏幕 */
.large-text {
  font-size: 20vw; /* 字体大小是屏幕宽度的 20% */
  font-weight: bold;
  color: black;
}
</style>
