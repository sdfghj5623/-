<template>
  <view class="container">
    <view class="title">用户注册</view>

    <!-- 账号输入框 -->
    <view class="input-group">
      <input
        type="text"
        v-model="username"
        placeholder="请输入账号(必填)"
        class="input"
      />
    </view>

    <!-- 昵称输入框 -->
    <view class="input-group">
      <input
        type="text"
        v-model="nickname"
        placeholder="请输入昵称"
        class="input"
      />
    </view>

    <!-- 密码输入框 -->
    <view class="input-group">
      <input
        type="password"
        v-model="password"
        placeholder="请输入密码(必填)"
        class="input"
      />
    </view>

    <!-- 确认密码输入框 -->
    <view class="input-group">
      <input
        type="password"
        v-model="confirmPassword"
        placeholder="请再次输入密码(必填)"
        class="input"
      />
    </view>

    <!-- 同意协议勾选框 -->
    <view class="agreement">
      <checkbox @tap="toggleAgree" class="checkbox"></checkbox>
      <text class="agreement-text">同意</text>
      <text class="clickable" @tap="onClick">用户协议</text>
      <text class="agreement-text">和</text>
      <text class="clickable" @tap="onClick">隐私政策条款</text>
    </view>

    <!-- 注册按钮 -->
    <view class="register-button">
      <button @click="register" class="btn-login">注册</button>
    </view>

    <!-- 返回按钮 -->
    <view class="back-button">
      <button @click="back" class="back-login">返回</button>
    </view>

  </view>
</template>

<script>
export default {
  data() {
    return {
      username: "",  // 用户名
      nickname: "",  // 昵称
      password: "",  // 密码
      confirmPassword: "",  // 确认密码
      agree: false,  // 是否同意协议
    };
  },
  methods: {
    // 注册方法
register() {
  console.log('Register button clicked'); // 确认按钮点击事件触发

  // 检查账号和密码是否为空
  if (!this.username || !this.password) {
    uni.showToast({
      title: "账号和密码不能为空",
      icon: "none",
    });
    return;
  }

  // 检查账号长度是否为10位
  if (this.username.length !== 10) {
    uni.showToast({
      title: "账号必须是10位",
      icon: "none",
    });
    return;
  }

  // 检查两次密码是否一致
  if (this.password !== this.confirmPassword) {
    uni.showToast({
      title: "两次密码输入不一致",
      icon: "none",
    });
    return;
  }

  // 检查是否同意协议
  if (!this.agree) {
    uni.showToast({
      title: "请同意用户协议和隐私政策",
      icon: "none",
    });
    return;
  }

  const userData = {
    zhanghao: this.username, // 使用正确的字段名
    nickname: this.nickname,
    password: this.password,
  };

  console.log("Sending registration data:", JSON.stringify(userData, null, 2)); // 打印发送的数据

  uni.request({
    url: 'http://127.0.0.1:5000/api/register',  // Flask API 地址
    method: 'POST',
    data: userData,
    header: {
      'content-type': 'application/json'  // 设置请求头为JSON格式
    },
    success: (res) => {
      console.log("Server response:", res); // 打印服务器响应
      if (res.statusCode === 201) {
        uni.showToast({
          title: "注册成功",
          icon: "success",
        });

        // 跳转到首页
        uni.navigateTo({
          url: '/pages/log/log'
        });
      } else {
        uni.showToast({
          title: "注册失败，账号已被注册",
          icon: "none",
        });
      }
    },
    fail: (err) => {
      console.error("Request failed:", err); // 打印错误信息
      uni.showToast({
        title: "网络请求失败",
        icon: "none",
      });
    }
  });
},

    // 返回按钮
    back() {
      uni.navigateTo({
        url: '/pages/log/log'
      });
    },

    // 同意协议复选框变化
    toggleAgree() {
      this.agree = !this.agree;
    },

    // 点击用户协议或隐私政策
    onClick() {
      uni.navigateTo({
        url: "/pages/lan/lan",
      });
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  height: 100vh;
}

.title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: left;
  width: 90%;
  color: #000000;
}

.input-group {
  width: 90%;
  margin-bottom: 20px;
  background-color: #ddd;
}

.clickable {
  font-size: 14px;
  color: blue;
  text-decoration: underline;
  cursor: pointer;
}

.input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid rgb(248,248,248);
  border-radius: 4px;
  background-color: rgb(248,248,248);
}

.agreement {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  width: 90%;
}

.checkbox {
  margin-right: 10px;
}

.agreement-text {
  font-size: 14px;
  color: #666;
}

.register-button {
  width: 90%;
  margin-bottom: 20px;
}

.back-button {
  width: 90%;
  margin-bottom: 20px;
}

.btn-login {
  width: 100%;
  padding: 5px;
  background-color: #007aff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.btn-login:hover {
  background-color: #005bb5;
}

.footer {
  display: flex;
  justify-content: space-between;
  width: 80%;
  font-size: 14px;
  color: #007aff;
}

.footer-link {
  cursor: pointer;
}

.footer-link:hover {
  text-decoration: underline;
}
</style>
