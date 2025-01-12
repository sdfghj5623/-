<template>
  <view class="container">
    <view class="title">绑定手机号</view>

    <!-- 账号输入框 -->
    <view class="input-group">
      <input
        type="text"
        v-model="username"
        placeholder="请输入手机号"
        class="input"
      />
    </view>

    <!-- 昵称输入框 -->
    <view class="input-group">
      <input
        type="text"
        v-model="nickname"
        placeholder="请输入验证码"
        class="input"
      />
    </view>

    
<!--    <view class="input-group">
      <input
        type="password"
        v-model="password"
        placeholder="请输入新密码(必填)"
        class="input"
      />
    </view> -->

    <!-- 确认密码输入框 -->
<!--    <view class="input-group">
      <input
        type="password"
        v-model="confirmPassword"
        placeholder="请再次输入新密码(必填)"
        class="input"
      />
    </view> -->

    <!-- 同意协议勾选框 -->
   <!-- <view class="agreement">
      <checkbox @tap="toggleAgree" class="checkbox"></checkbox>
      <text class="agreement-text">同意</text>
      <text class="clickable" @tap="onClick">用户协议</text>
      <text class="agreement-text">和</text>
      <text class="clickable" @tap="onClick">隐私政策条款</text>
    </view> -->

    <!-- 注册按钮 -->
    <view class="register-button">
      <button @click="register" class="btn-login">提交</button>
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
    if (!this.username) {
        uni.showToast({
            title: "手机号不能为空",
            icon: "none",
        });
        return;
    } else if (this.username.length != 11) {
        uni.showToast({
            title: "手机号位数不正确",
            icon: "none",
        });
        return;
    } else if (!this.nickname) {
        uni.showToast({
            title: "请输入验证码",
            icon: "none",
        });
        return;
    } else if (this.nickname != 335200) {
        uni.showToast({
            title: "验证码不正确",
            icon: "none",
        });
        return;
    } else {
		let user = uni.getStorageSync('user');
		console.log(user);  // 输出存储的用户信息
		let id = user.id;  // 获取用户ID
        uni.request({
            url: `http://127.0.0.1:5000/api/user_info_update_mobile/${id}`,
            method: 'PUT',
            data: {
                mobile: this.username,
            },
            success: (res) => {
                console.log('res', res);
                
                // 如果返回的数据中有错误信息（例如手机号已注册），显示提示
                if (res.data.error) {
                    uni.showToast({
                        title: res.data.error,
                        icon: 'none'
                    });
                } else {
                    // 如果手机号更新成功
                    uni.showToast({
                        title: '绑定成功',
                        icon: 'none'
                    });
                }
            },
            fail: (err) => {
                console.log('请求失败:', err);
                uni.showToast({
                    title: '请求失败，请稍后重试',
                    icon: 'none'
                });
            }
        });

        // 页面跳转
        setTimeout(() => {
          uni.reLaunch({
            url: "/pages/self/self"
          });
        }, 800);
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
