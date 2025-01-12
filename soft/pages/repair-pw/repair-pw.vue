<template>
  <view class="container">
    <view class="title">修改密码</view>

    <!-- 账号输入框 -->
    <view class="input-group">
      <input
        type="text"
        v-model="username"
        placeholder="请输入旧密码"
        class="input"
      />
    </view>

    <!-- 昵称输入框 -->
<!--    <view class="input-group">
      <input
        type="text"
        v-model="nickname"
        placeholder="请输入验证码"
        class="input"
      />
    </view> -->

    <!-- 密码输入框 -->
    <view class="input-group">
      <input
        type="password"
        v-model="password"
        placeholder="请输入新密码"
        class="input"
      />
    </view>

    <!-- 确认密码输入框 -->
    <view class="input-group">
      <input
        type="password"
        v-model="confirmPassword"
        placeholder="请再次输入新密码"
        class="input"
      />
    </view>

    <!-- 同意协议勾选框 -->
<!--    <view class="agreement">
      <checkbox @tap="toggleAgree" class="checkbox"></checkbox>
      <text class="agreement-text">同意</text>
      <text class="clickable" @tap="onClick">用户协议</text>
      <text class="agreement-text">和</text>
      <text class="clickable" @tap="onClick">隐私政策条款</text>
    </view> -->

    <!-- 注册按钮 -->
    <view class="register-button">
      <button @click="register" class="btn-login">重置</button>
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
      // 检查账号和密码是否为空
      if (!this.username || !this.password) {
        uni.showToast({
          title: "密码不能为空",
          icon: "none",
        });
        return;
      }

      // 检查两次密码是否一致
      else if (this.password !== this.confirmPassword) {
        uni.showToast({
          title: "两次密码输入不一致",
          icon: "none",
        });
        return;
      }
	  
else{
let user = uni.getStorageSync('user');
console.log(user);  // 输出存储的用户信息
let id = user.id;  // 获取用户ID

uni.request({
    url: `http://127.0.0.1:5000/api/user_info_update_password/${id}`,
    method: 'PUT',
    data: {
        oldpassword: this.username,  // 假设oldpassword为旧密码
        newpassword: this.password   // 假设newpassword为新密码
    },
    success: (res) => {
        console.log('res', res);
        if (res.data.message === '密码更新成功') {
            uni.showToast({
                title: '修改成功',
                icon: 'none'
            });
			setTimeout(() => {
			  uni.reLaunch({
			    url: "/pages/self/self"
			  });
			}, 800);
        }
		else if (res.data.error === '旧密码不正确') {
            uni.showToast({
                title: '旧密码不正确',
                icon: 'none'
            });
			// setTimeout(() => {
   //    uni.navigateTo({
   //      url: '/pages/user_info/user_info'
   //    });
			// }, 800);
        }
    },
    fail: (err) => {
        console.log('请求失败:', err);
        // 检查返回的错误信息
        if (err && err.data && err.data.error) {
            // 如果是旧密码错误
            if (err.data.error === '旧密码不正确') {
                uni.showToast({
                    title: '旧密码不正确',
                    icon: 'none'
                });
            } else {
                uni.showToast({
                    title: '请求失败，请稍后重试',
                    icon: 'none'
                });
            }
        } else {
            uni.showToast({
                title: '请求失败，请稍后重试',
                icon: 'none'
            });
        }
    }
});

      // 跳转到首页
    }
	},

    // 返回按钮
    back() {
      uni.navigateTo({
        url: '/pages/user_info/user_info'
      });
    },

    // 同意协议复选框变化
    toggleAgree() {
      this.agree = !this.agree;
    },

    // 点击用户协议或隐私政策
    onClick() {
      // 跳转到协议或隐私政策页面的逻辑
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
