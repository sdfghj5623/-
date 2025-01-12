<template>
	<view class="uni-content">
		<template v-if="verifyFail">
			<view class="face-icon">
				<image src="./face-verify-icon.svg" class="face-icon-image" />
			</view>
			<view class="error-title">{{verifyFailTitle}}</view>
			<view class="error-description">{{verifyFailContent}}</view>
			<button type="primary" @click="retry" v-if="verifyFailCode !== 10013">重新开始验证</button>
			<button type="primary" @click="retry" v-else>返回</button>
			<view class="dev-tip" v-if="isDev">请在控制台查看详细错误（此提示仅在开发环境展示）</view>
		</template>
		<template v-else>
			<view class="self-required" v-if="realName">确认<text class="name">{{realNameDesensitized}}</text>本人操作</view>
			<view class="face-icon">
				<image src="./face-verify-icon.svg" class="face-icon-image" />
			</view>
			<view class="suggestion">
				<view class="text">温馨提示</view>
				<view class="text" v-for="text in suggestion">
					<text class="dot"></text>
					<text>{{text}}</text>
				</view>
			</view>
			<view class="footer">
				<button type="primary" :disabled="verifyButtonDisabled" @click="getCertifyId">开始人脸识别</button>
			</view>
		</template>
	</view>
</template>

<script>
	import {
		mutations
	} from '@/uni_modules/uni-id-pages/common/store.js'
	import checkIdCard from '@/uni_modules/uni-id-pages/common/check-id-card.js'
	const uniIdCo = uniCloud.importObject('uni-id-co')
	const tempFrvInfoKey = 'uni-id-pages-temp-frv'

	export default {
		data() {
			return {
				realName: "",
				idCard: "",
				certifyId: "",
				suggestion: [
					"请正对屏幕并使脸位于取景框内",
					"请保持光线充足，避免光照过强或过弱",
					"请根据画面提示完成动作检测",
					"人脸识别过程中请保持手机稳定",
					"请注意拍摄角度，距离摄像头不要过远或过近"
				],
				verifyFail: false,
				verifyFailCode: 0,
				verifyFailTitle: "",
				verifyFailContent: ""
			}
		},
		computed: {
			realNameDesensitized() {
				const firstChar = this.realName.slice(0, -1)
				const lastChar = this.realName.slice(-1)
				return Array.from(new Array(firstChar.length), (v) => '*').join('') + lastChar
			},
			verifyButtonDisabled() {
				return !this.realName || !this.idCard
			},
			isDev () {
				return process.env.NODE_ENV === 'development'
			}
		},
		onLoad(e) {
			this.realName = e.realName || ''
			this.idCard = e.idCard || ''
		},
		methods: {
			async getCertifyId() {
				if (!this.realName || !this.idCard) {
					uni.showModal({
						title: "验证失败",
						content: "缺少姓名或身份证号码",
						showCancel: false
					})
					return
				}

				if (!checkIdCard(this.idCard)) {
					uni.showToast({
						title: "身份证不合法",
						icon: "none"
					})
					return
				}

        if (!/^[\u4e00-\u9fa5]+$/.test(this.realName)) {
          uni.showToast({
            title: "姓名只能是汉字",
            icon: "none"
          })
          return
        }

				const res = await uniIdCo.getFrvCertifyId({
					realName: this.realName,
					idCard: this.idCard
				})

				this.certifyId = res.certifyId

				this.startFacialRecognitionVerify()

				uni.setStorage({
					key: tempFrvInfoKey,
					data: {
						realName: this.realName,
						idCard: this.idCard
					}
				});
			},
			startFacialRecognitionVerify() {
				// 每次刷脸重置状态
				this.verifyFailCode = 0
				this.verifyFail = false
				this.verifyFailTitle = ''
				this.verifyFailContent = ''

				// #ifdef APP
				uni.startFacialRecognitionVerify({
					certifyId: this.certifyId,
					quitAlertMessage: " ",
					quitAlertTitle: "确定退出吗？",
					success: (e) => {
						this.getFrvAuthResult()
					},
					fail: (e) => {
						let title = "验证失败"
						let content

						console.log(`[frv-debug] certifyId auth error: certifyId -> ${this.certifyId}, error -> ${JSON.stringify(e, null, 4)}`)

						switch (e.errCode) {
							case 10001:
								content = '认证ID为空'
								break
							case 10010:
								title = '刷脸异常'
								content = e.cause.message || '错误代码: 10010'
								break
							case 10011:
								title = '验证中断'
								content = e.cause.message || '错误代码: 10011'
								break
							case 10012:
								content = '网络异常'
								break
							case 10013:
								this.verifyFailCode = e.errCode
								this.verifyFailContent = e.cause.message || '错误代码: 10013'
								this.getFrvAuthResult()

								console.log(`[frv-debug] 刷脸失败, certifyId -> ${this.certifyId}, 如在开发环境请检查用户的姓名、身份证号与刷脸用户是否为同一用户。如遇到认证ID已使用请检查opendb-frv-logs表中certifyId状态`)
								return
							case 10020:
								content = '设备设置时间异常'
								break
							default:
								title = ''
								content = `验证未知错误 (${e.errCode})`
								break
						}

						this.verifyFail = true
						this.verifyFailCode = e.errCode
						this.verifyFailTitle = title
						this.verifyFailContent = content
					}
				})
				// #endif
			},
			async getFrvAuthResult() {
				const uniIdCo = uniCloud.importObject('uni-id-co', {
					customUI: true
				})
				try {
					uni.showLoading({
						title: "验证中...",
						mask: false
					})
					const res = await uniIdCo.getFrvAuthResult({
						certifyId: this.certifyId
					})

					const {
						errCode,
						...rest
					} = res

					if (this.verifyFailContent) {
						console.log(`[frv-debug] 客户端刷脸失败，由实人认证服务查询具体原因，原因：${this.verifyFailContent}`)
					}

					uni.showModal({
						content: "实名认证成功",
						showCancel: false,
						success: () => {
							mutations.setUserInfo({
								realNameAuth: rest
							})
							uni.navigateBack(-1)
						}
					})

					uni.removeStorage({
						key: tempFrvInfoKey
					})
				} catch (e) {
					this.verifyFail = true
					this.verifyFailTitle = e.errMsg
					console.error(JSON.stringify(e));
				} finally {
					uni.hideLoading()
				}
			},
			retry() {
				if (this.verifyFailCode !== 10013) {
					this.startFacialRecognitionVerify()
				} else {
					uni.navigateBack(-1)
				}
			}
		},
	}
</script>

<style lang="scss">
	@import "@/uni_modules/uni-id-pages/common/login-page.scss";

	.self-required {
		margin-top: 20px;
		font-size: 18px;
		font-weight: bold;
		text-align: center;
		color: #333333;

		.name {
			color: #2979ff
		}
	}

	.face-icon {
		width: 100px;
		height: 100px;
		margin: 50px auto 30px;
	}

	.face-icon-image {
		width: 100%;
		height: 100%;
		display: block;
	}

	.suggestion {
		color: #999999;
		font-size: 13px;
		margin-bottom: 20px;

		.text {
			line-height: 20px;
			display: flex;
			align-items: center;

			.dot {
				width: 5px;
				height: 5px;
				background: #2979ff;
				border-radius: 50%;
				margin-right: 5px;
			}
		}
	}

	.error-title {
		font-size: 18px;
		text-align: center;
		font-weight: bold;
	}

	.error-description {
		font-size: 13px;
		color: #999999;
		margin: 10px 0 20px;
		text-align: center;
	}
	.dev-tip {
		margin-top: 20px;
		font-size: 13px;
		color: #999;
		text-align: center;
	}
</style>
