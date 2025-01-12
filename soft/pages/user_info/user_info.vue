<template>
  <view class="container">
    <!-- 用户头像 -->
    <view class="profile-header" @tap="repairava">
      <image  class="avatar" :src="user.userInfo_user_pic || '../../static/images/user-default.jpg'" alt="用户头像" />
    </view>
    
    <!-- 用户信息 -->
    <view class="user-info">
      <!-- 昵称 -->
      <view class="info-row" @click="openNicknameModal">
        <text class="label">昵称：</text>
        <text class="value">{{ user.userInfo_user_nickname || '匿名用户' }} ></text>
      </view>

      <!-- 手机号 -->
      <view class="info-row" @click="editmobile">
        <text class="label">手机号：</text>
        <text class="value">{{ user.userInfo_user_mobile || '未绑定' }} ></text>
      </view>

      <!-- 修改密码 -->
      <view class="info-row" @click="editPassword">
        <text class="label">修改密码：</text>
        <text class="value">点击修改 ></text>
      </view>

      <!-- 注销账号 -->
      <view class="info-row" @click="logoutAccount">
        <text class="label">注销账号：</text>
        <text class="value">点击注销 ></text>
      </view>
    </view>

    <!-- 昵称修改弹框 -->
    <view v-if="isModalVisible" class="modal-overlay" @click="closeNicknameModal">
      <view class="modal" @click.stop>
        <text class="modal-title">修改昵称</text>
        <input class="modal-input" v-model="newNickname" placeholder="请输入新昵称" />
        <view class="modal-actions">
          <button class="modal-button-cancle" @click="updateNickname">确认</button>
          <button class="modal-button-sure" @click="closeNicknameModal">取消</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      user: {
				userInfo_user_pic:'',
				userInfo_user_nickname:'',
				userInfo_user_mobile:'',
      },
      isModalVisible: false,  // 控制弹框的显示与隐藏
      newNickname: '',       // 存储新昵称的值
	  files:'',
    };
  },
  onLoad(){
  	this.userInfo()
  },
  methods: {
 userInfo() {
        console.log("12312");
        let user = uni.getStorageSync('user');
        console.log(user);  // 输出存储的用户信息
        let id = user.id;

        // 发起请求
        uni.request({
            url: `http://127.0.0.1:5000/api/user_info_get/${id}`,
            method: 'GET',
            success: (res) => {
                console.log('res', res.data);

                // 判断用户头像是否有效
                let userPic = res.data.user_info.user_pic && typeof res.data.user_info.user_pic === 'string' && res.data.user_info.user_pic.trim() !== ''
                    ? `data:image/jpeg;base64,${res.data.user_info.user_pic.trim()}`
                    : null;

                // 更新用户信息
                this.user.userInfo_user_nickname = res.data.user_info.user_nickname[0];  // 这里更新的是正确的对象
                console.log("user", this.user.userInfo_user_nickname);
                this.user.userInfo_user_pic = userPic; // 处理头像
                this.user.userInfo_user_mobile = res.data.user_info.user_mobile[0];
            },
            fail: (err) => {
                console.log('请求失败:', err);
                uni.showToast({
                    title: '请求失败，请稍后重试',
                    icon: 'none'
                });
            }
        });
    },
	
repairava() {
    console.log("12312");
    let user = uni.getStorageSync('user');
    console.log(user);  // 输出存储的用户信息
    let id = user.id;

    uni.chooseImage({
        count: 1,
        sourceType: ['album', 'camera'],
        success: async (res) => {
            this.user.userInfo_user_pic = res.tempFilePaths[0];  // 保存图片路径
            const selectedImagePath = res.tempFilePaths[0];  // 获取选中的图片路径

            // 通过 fetch 获取 Blob 对象
            const blob = await fetch(selectedImagePath).then((res) => res.blob());
            console.log("图片 Blob 数据: ", blob);  // 打印 blob 对象进行调试

            // 将 Blob 转换为 Base64
            const base64Data = await this.blobToBase64(blob); // 新增：将 Blob 转为 Base64 编码
            console.log("图片 Base64 数据: ", base64Data);  // 打印 Base64 编码进行调试

            // 发起请求，传递 Base64 编码数据
            uni.request({
                url: `http://127.0.0.1:5000/api/user_info_update_avatar/${id}`,
                method: 'PUT',
                data: {
                    avatar: base64Data,  // 将 Base64 编码的头像传递给后端
                },
                success: (res) => {
                    console.log('res', res);
                    uni.showToast({
                        title: '更新成功',
                        icon: 'none'
                    });
                },
                fail: (err) => {
                    console.log('请求失败:', err);
                    uni.showToast({
                        title: '更新失败',
                        icon: 'none'
                    });
                }
            });

        },
        fail: (err) => {
            console.log(err);
            uni.showToast({
                title: '更新失败',
                icon: 'none'
            });
        },
    });
},

// Blob 转换为 Base64 编码的函数
async blobToBase64(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);  // 去掉数据URI的前缀部分
        reader.onerror = reject;
        reader.readAsDataURL(blob);  // 读取文件为 Base64 数据
    });
},

	
	// 将 Blob 转换为 File 对象
	blobToFile(blob, filename) {
	  return new Promise((resolve, reject) => {
	    const reader = new FileReader();
	    reader.onloadend = function () {
	      const file = new File([reader.result], filename, { type: blob.type });
	      resolve(file);
	    };
	    reader.onerror = reject;
	    reader.readAsArrayBuffer(blob);
	  });
	},
	  
    openNicknameModal() {
      // 打开修改昵称的弹框
      this.isModalVisible = true;
      this.newNickname = this.user.nickname;  // 预填当前昵称
    },
    closeNicknameModal() {
      // 关闭修改昵称的弹框
      this.isModalVisible = false;
      this.newNickname = ''; // 清空输入框
    },
    updateNickname() {
      // 更新昵称并关闭弹框
	  console.log("12312");
	  let user = uni.getStorageSync('user');
	  console.log(user);  // 输出存储的用户信息
	  let id = user.id;
	  uni.request({
	      url: `http://127.0.0.1:5000/api/user_info_update_nickname/${id}`,
	      method: 'PUT',
	      data: {
	          nickname: this.newNickname,  
	      },
	      success: (res) => {
			  this.user.userInfo_user_nickname = this.newNickname;
	              uni.showToast({
	                  title: '修改成功',
	                  icon: 'none'
	              });
				  if (this.newNickname.trim()) {
				    this.user.nickname = this.newNickname;
				    this.closeNicknameModal();
				    console.log('昵称已更新为:', this.newNickname);
				  } else {
				    alert('昵称不能为空');
				  }

	      },
	      fail: (err) => {
	                  uni.showToast({
	                      title: '请求失败，请稍后重试',
	                      icon: 'none'
	                  });   
	      }
	  });
    },
    editPassword() {
		uni.navigateTo({
			url: '/pages/repair-pw/repair-pw'
		})	
      console.log('修改密码');
    },
	editmobile(){
		uni.navigateTo({
					url: '/pages/mobile/mobile'
				})	
		console.log('绑定手机');
	},
    logoutAccount() {
		uni.showModal({
			title:"是否确认注销?",
			success:res=>{
				console.log("12312");
				let user = uni.getStorageSync('user');
				console.log(user);  // 输出存储的用户信息
				let id = user.id;
				console.log(res);
				if(res.confirm){
					uni.request({
					    url: `http://127.0.0.1:5000/api/delete_user_info/${id}`,
					    method: 'DELETE',
					    success: (res) => {
					            uni.showToast({
					                title: '注销成功',
					                icon: 'none'
					            });
								uni.navigateTo({
											url: '/pages/log/log'
										})	
					
					    },
					    fail: (err) => {
					                uni.showToast({
					                    title: '请求失败，请稍后重试',
					                    icon: 'none'
					                });   
					    }
					});

				}
			}
		})
      console.log('注销账号');
    },
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-header {
  margin-bottom: 20px;
}

.avatar {
  width: 200px;
  height: 200px;
/*  border-radius: 50%; */
  object-fit: cover;
  margin-top: 60px;
}

.user-info {
  width: 100%;
  margin-top: 50px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-bottom: 2px solid #f0f0f0;
}

.label {
  font-weight: bold;
  font-size: 16px;
}

.value {
  font-size: 16px;
  color: #666;
}

.info-row:hover {
  background-color: #f9f9f9;
  cursor: pointer;
}

/* 弹框相关样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 400px;
  text-align: center;
}

.modal-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}

/* 输入框样式 */
.modal-input {
  width: 100%; /* 使输入框占满父容器宽度 */
  max-width: 300px; /* 可以设置最大宽度，避免过长的输入框 */
  padding: 8px;
  font-size: 16px;
  margin-bottom: 20px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-left: auto; /* 确保居中 */
  margin-right: auto; /* 确保居中 */
}

/* 按钮容器样式 */
.modal-actions {
  display: flex;
  justify-content: center; /* 确保按钮居中 */
  gap: 20px; /* 设置按钮之间的间距 */
}

/* 取消按钮样式 */
.modal-button-cancle {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #ffffff;
  color: black;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  height: 40px;
  width: 100px;
  text-align: center; /* 确保文字居中 */
  /* 使用 flexbox 来居中对齐文字 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  
  text-align: center; /* 确保文字水平居中 */
}

/* 确认按钮样式 */
.modal-button-sure {
  padding: 0; /* 去掉默认的 padding，使 flexbox 能够正常工作 */
  font-size: 16px;
  background-color: #ffffff;
  color: blue;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  height: 40px;
  width: 100px;
  
  /* 使用 flexbox 来居中对齐文字 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  
  text-align: center; /* 确保文字水平居中 */
}


/* 按钮 hover 效果 */
.modal-button-cancle:hover,
.modal-button-sure:hover {
  background-color: #f0f0f0;
}

</style>
