<template>
  <view>
    <web-view :src="webUrl"></web-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      webUrl: ''
    };
  },
  onLoad(options) {
    // 通过 options 获取跳转时传递的 URL 参数
    this.webUrl = options.url ? decodeURIComponent(options.url) : '';
  }
};
</script>
