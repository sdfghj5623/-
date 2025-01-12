<template>
  <view>
    <template v-if="isCertify">
      <uni-list>
        <uni-list-item class="item" title="姓名" :rightText="userInfo.realNameAuth.realName"></uni-list-item>
        <uni-list-item class="item" title="身份证号码" :rightText="userInfo.realNameAuth.identity"></uni-list-item>
      </uni-list>
    </template>
    <template v-else>
      <view class="uni-content">
        <text class="title">实名认证</text>
        <uni-forms>
          <uni-forms-item name="realName">
            <uni-easyinput placeholder="姓名" class="input-box" v-model="realName" :clearable="false">
            </uni-easyinput>
          </uni-forms-item>
          <uni-forms-item name="idCard">
            <uni-easyinput placeholder="身份证号码" class="input-box" v-model="idCard" :clearable="false">
            </uni-easyinput>
          </uni-forms-item>
        </uni-forms>
        <uni-id-pages-agreements scope="realNameVerify" ref="agreements" style="margin-bottom: 20px;">
        </uni-id-pages-agreements>
        <button type="primary" :disabled="!certifyIdNext" @click="goToFaceVerifyPage">确定</button>
      </view>
    </template>
  </view>
</template>

<script>
import checkIdCard from '@/uni_modules/uni-id-pages/common/check-id-card.js'
import mixin from '@/uni_modules/uni-id-pages/common/login-page.mixin.js';
import {store} from '@/uni_modules/uni-id-pages/common/store.js'

const uniIdCo = uniCloud.importObject('uni-id-co')
const tempFrvInfoKey = 'uni-id-pages-temp-frv'
export default {
  mixins: [mixin],
  data() {
    return {
      realName: '',
      idCard: ''
    }
  },
  computed: {
    userInfo() {
      return store.userInfo
    },
    certifyIdNext() {
      return Boolean(this.realName) && Boolean(this.idCard) && (this.needAgreements && this.agree)
    },
    isCertify() {
      return this.userInfo.realNameAuth && this.userInfo.realNameAuth.authStatus === 2
    }
  },
  onLoad() {
    const tempFrvInfo = uni.getStorageSync(tempFrvInfoKey);
    if (tempFrvInfo) {
      this.realName = tempFrvInfo.realName
      this.idCard = tempFrvInfo.idCard
    }
  },
  methods: {
    async goToFaceVerifyPage() {
      if (!this.certifyIdNext) return

      // #ifndef APP
      return uni.showModal({
        content: "暂不支持实名认证",
        showCancel: false
      })
      // #endif

      if (!checkIdCard(this.idCard)) {
        uni.showToast({
          title: "身份证不合法",
          icon: "none"
        })
        return
      }

      if (
          typeof this.realName !== 'string' ||
          this.realName.length < 2 ||
          !/^[\u4e00-\u9fa5]{1,10}(·?[\u4e00-\u9fa5]{1,10}){0,5}$/.test(this.realName)
      ) {
        uni.showToast({
          title: "姓名只能是汉字",
          icon: "none"
        })
        return
      }

      uni.navigateTo({
        url: '/uni_modules/uni-id-pages/pages/userinfo/face-verify/face-verify?realName=' + this
            .realName + '&idCard=' + this.idCard
      });
    }
  }
}
</script>

<style lang="scss">
@import "@/uni_modules/uni-id-pages/common/login-page.scss";

.checkbox-box,
.uni-label-pointer {
  align-items: center;
  display: flex;
  flex-direction: row;
}

.item {
  flex-direction: row;
}

.text {
  line-height: 26px;
}

.checkbox-box ::v-deep .uni-checkbox-input {
  border-radius: 100%;
}

.checkbox-box ::v-deep .uni-checkbox-input.uni-checkbox-input-checked {
  border-color: $uni-color-primary;
  color: #FFFFFF !important;
  background-color: $uni-color-primary;
}

.agreements {
  margin-bottom: 20px;
}
</style>
