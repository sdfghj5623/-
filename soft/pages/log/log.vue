<template>
  <view class="container">
    <!-- 账号密码登录标题 -->
    <view class="title">账号密码登录</view>

    <!-- 手机号输入框 -->
    <view class="input-group">
      <input
        type="text"
        v-model="username"
        placeholder="请输入账号/手机号"
        class="input"
      />
    </view>

    <!-- 密码输入框 -->
    <view class="input-group">
      <input
        type="password"
        v-model="password"
        placeholder="请输入密码"
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

    <!-- 登录按钮 -->
    <view class="login-button">
      <button @click="handleLogin" class="btn-login">登录</button>
    </view>

    <!-- 找回密码和注册账号 -->
    <view class="footer">
      <view class="left">
        <text @click="goToForgotPassword" class="footer-link">找回密码</text>
      </view>
      <view class="right">
        <text @click="goToRegister" class="footer-link">注册账号</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      agree: false,
    };
  },
  methods: {
    handleLogin() {
      if (!this.username || !this.password) {
        uni.showToast({
          title: "手机号和密码不能为空",
          icon: "none",
        });
        return;
      }

      if (!this.agree) {
        uni.showToast({
          title: "请同意用户协议和隐私政策",
          icon: "none",
        });
        return;
      }

      // 登录逻辑
      const loginData = {
        zhanghao: this.username, // 使用正确的字段名
        password: this.password,
      };

      uni.request({
        url: 'http://127.0.0.1:5000/api/login', // Flask API 地址
        method: 'POST',
        data: loginData,
        header: {
          'content-type': 'application/json' // 设置请求头为JSON格式
        },
        success: (res) => {
          console.log("Server response:", res); // 打印服务器响应
          if (res.statusCode === 200) {
            uni.showToast({
              title: "登录成功",
              icon: "success",
            });

            // 保存用户信息到本地存储或管理状态（视应用架构而定）
            uni.setStorageSync('user', res.data.user);

            // 跳转到首页
	            		setTimeout(()=>{
	            			uni.reLaunch({
	            				url:"/pages/news/news"
	            			})
	            		},800)
          } else {
            uni.showToast({
              title: res.data.error || "登录失败，请稍后再试",
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
    onClick() {
      uni.navigateTo({
        url: "/pages/lan/lan",
      });
    },

    toggleAgree(e) {
      console.log('Checkbox changed:', e);
      this.agree = !this.agree;
      console.log(this.agree);
    },

    goToForgotPassword() {
      uni.navigateTo({
        url: "/pages/searchpw/searchpw",
      });
    },

    goToRegister() {
      uni.navigateTo({
        url: "/pages/register/register",
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

.login-button {
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
