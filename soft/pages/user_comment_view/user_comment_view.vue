<template>
  <view>
    <view v-if="userComments && userComments.length">
      <view v-for="(comment, index) in userComments" :key="index" class="user-comment">
        <text><strong>Nickname:</strong> {{ comment.user_nickname }}</text>
        <text><strong>Comment:</strong> {{ comment.comment_content }}</text>
        <text><strong>Date:</strong> {{ formatDate(comment.comment_date) }}</text>
      </view>
    </view>
    <view v-else>
      <text>加载失败，请稍后再试</text>
    </view>
  </view>
</template>

<script>
import axios from 'axios'; 
export default {
  data() {
    return {
      userComments: [],  // 保存获取到的多个评论数据
    };
  },
  methods: {
    formatDate(timestamp) {
      console.log(timestamp);
      const validTimestamp = Number(timestamp);  // 转换为数字
      const date = new Date(validTimestamp);
      
      // 获取月份、日期、小时、分钟和秒，且都使用 padStart 补充0，确保是两位数
      const month = (date.getMonth() + 1).toString().padStart(2, '0');  // 月份从0开始，所以+1，并补充0
      const day = date.getDate().toString().padStart(2, '0');  // 补充0
      const hours = date.getHours().toString().padStart(2, '0');  // 获取小时并补充0
      const minutes = date.getMinutes().toString().padStart(2, '0');  // 获取分钟并补充0
      const seconds = date.getSeconds().toString().padStart(2, '0');  // 获取秒数并补充0
      
      return `${month}-${day} ${hours}:${minutes}:${seconds}`;  // 格式化为 MM-DD HH:mm:ss
    },
    getData() {
      // 从本地存储中获取用户信息
      let user = uni.getStorageSync('user');
      console.log(user);  // 输出存储的用户信息

      if (user && user.id) {
        // 发送 GET 请求到后端 API
        axios.get(`http://127.0.0.1:5000/api/user_comment?user_id=${user.id}`)
          .then(res => {
            console.log("API Response:", res.data); // 输出API响应以进行调试
            if (res.data.user_comments && res.data.user_comments.length > 0) {
              this.userComments = res.data.user_comments;  // 将返回的评论列表存储到 userComments 中
            } else {
              uni.showToast({
                title: '没有找到该用户的评论',
                icon: 'none',
                duration: 2000
              });
            }
          })
          .catch(error => {
            console.error("Error fetching data:", error);
            uni.showToast({
              title: '加载失败，请稍后再试',
              icon: 'none',
              duration: 2000,
            });
          });
      } else {
        uni.showToast({
          title: '用户信息无效',
          icon: 'none',
          duration: 2000,
        });
      }
    },
  },
  mounted() {
    this.getData();  // 页面加载时获取数据
  },
};
</script>

<style scoped>
.user-comment {
  margin: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.user-comment text {
  display: block;
  margin-bottom: 10px;
  font-size: 16px;
}
</style>
