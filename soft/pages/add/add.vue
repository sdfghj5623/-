<template>
  <view class="add">
    <form @submit="onSubmit">
      <!-- 表单项 -->
      <view class="item">
        <input v-model="formValue.title" type="text" name="title" placeholder="请输入完整的标题" />
      </view>

      <view class="item">
        <textarea maxlength="-1" v-model="formValue.content" name="content" placeholder="写点什么吧~"></textarea>
      </view>

      <!-- 图片选择按钮 -->
  <view class="image-picker">
    <!-- 图片上传区 -->
    <view class="image-container">
      <!-- 展示已选择的图片 -->
      <view v-for="(image, index) in previewImages" :key="index" class="image-item">
        <image :src="image" class="image-preview" @click="previewImage(index)" />
        <view class="delete-icon" @click.stop="removeImage(index)">×</view>
      </view>

      <!-- 如果没有上传图片，显示加号按钮 -->
      <view v-if="previewImages.length < 9" class="add-icon" @click="chooseImages">
        <text class="add-text">+</text>
      </view>
    </view>

    <!-- 上传图片的输入框（隐藏） -->
    <input type="file" accept="image/*" ref="fileInput" style="display:none" @change="onFileChange" />
  </view>

      <view class="item">
        <button form-type="reset" @click="resetForm">重置</button>
        <button form-type="submit" type="primary" :disabled="inDisabled(formValue)">确认发表</button>
      </view>
    </form>
  </view>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      imagePaths: [], // 存储选中的图片路径
      previewImages: [], // 存储预览图片的URL
      files: [], // 存储转换后的图片文件
      formValue: {
        title: "",
        content: ""
      }
    };
  },
  methods: {
    // 选择图片
	
	chooseImages() {
	  uni.chooseImage({
	    count: 9 - this.imagePaths.length, // 限制最多选择 9 张图片
	    success: async (res) => {
	      // 将新选择的图片路径追加到 imageValue 中
	      this.imagePaths = [...this.imagePaths, ...res.tempFilePaths];  // 保留之前的图片并追加新选择的图片
	
	      // 将预览图片更新
	      this.previewImages = [...this.imagePaths]; // 更新预览图片
	
	      // 对于每个图片路径，通过 fetch 获取 Blob 对象，再转换为 File
	      const filePromises = res.tempFilePaths.map(async (path) => {
	        const blob = await fetch(path).then((res) => res.blob()); // 获取 Blob 数据
	        console.log("图片 Blob 数据: ", blob); // 打印 blob 对象进行调试
	        return this.blobToFile(blob, 'image.jpg'); // 通过 `this` 调用 blobToFile 函数
	      });
	
	      // 将转换后的 File 对象追加到 files 数组
	      const newFiles = await Promise.all(filePromises);
	      this.files = [...this.files, ...newFiles];  // 保留之前的文件并追加新文件
	      console.log("转换后的文件列表: ", this.files); // 打印文件列表进行调试
	    }
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

    // 提交表单
    onSubmit(event) {
      if (event && typeof event.preventDefault === 'function') {
        event.preventDefault();  // 阻止默认行为
      }
	  let user = uni.getStorageSync('user');
	  let user_id = user.id;
	  console.log("user",user_id)
    
      const formData = new FormData();
      formData.append('title', this.formValue.title);
      formData.append('content', this.formValue.content);
      formData.append('publish_date', Date.now());
	  formData.append('user_id', user_id);
	  console.log('11',new Date(Date.now()))
    
      // 如果有文件，添加到 FormData 中
      if (this.files && this.files.length > 0) {
        this.files.forEach((file) => {
          formData.append('pictures[]', file);  // 将 File 对象添加到 FormData 中
        });
      }
    
      // 发送请求
      axios.post('http://127.0.0.1:5000/api/insert_quanzi_articles', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(res => {
        uni.showToast({
          title: "发布成功",
          icon: 'success',
          duration: 2000
        });
    
        setTimeout(() => {
          uni.reLaunch({
            url: "/pages/index/index"
          });
        }, 800);
      })
      .catch(error => {
        console.error("Error submitting form:", error);
        uni.showToast({
          title: "发布失败，请稍后再试",
          icon: 'none',
          duration: 2000
        });
      });
    },

    // 重置表单
    resetForm() {
      this.formValue = {
        title: "",
        content: ""
      };
      this.imagePaths = [];
      this.previewImages = [];
      this.files = [];
    },

    // 表单验证，判断是否启用提交按钮
    inDisabled(formValue) {
      return !formValue.title || !formValue.content;
    },
	
	// 删除图片
	removeImage(index) {
	  this.previewImages.splice(index, 1);  // 删除指定索引的图片
	  this.files.splice(index, 1);  // 删除对应的文件
	},
	
	// 预览图片
	previewImage(index) {
	  uni.previewImage({
	    current: index, // 当前预览图片的索引
	    urls: this.previewImages // 所有图片的URL
	  });
	}
  }
};
</script>

<style lang="scss" scoped>
.add{
	padding:30rpx;
	.item{
		padding-bottom:20rpx;
		input,textarea{
			border:1rpx solid #eee;
			height: 80rpx;
			padding:0 20rpx;
		}
		textarea{
			height: 200rpx;
			width: 100%;
			box-sizing: border-box;
		}
		button{
			margin-bottom:20rpx;
		}
	}
}

.preview-images {
  display: flex;
  flex-wrap: wrap;
}

.preview-image {
  width: 120px;
  height: 120px;
  margin-right: 10px;
  object-fit: cover;  /* 确保图片适应容器 */
}

.image-picker {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.image-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: flex-start;
  position: relative;
  width: 100%;
  min-height: 100px;
}

.add-icon {
  width: 120px;
  height: 120px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  border-radius: 8px;
  border: 1px solid #ccc;
  cursor: pointer;
  margin-bottom: 10px;
}

.add-text {
  font-size: 36px;
  color: #f0f0f0;
}

.image-item {
  position: relative;
}

.image-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
    margin-bottom: 10px;
}

.delete-icon {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
}

.add-icon {
  margin-left: 10px;
}

</style>
