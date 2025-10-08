<template>
    <div class="login-container">
        <div class="login-wrapper">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-4 col-md-6">
                        <!-- 登录卡片 -->
                        <div class="login-card">
                            <!-- 头部 -->
                            <div class="login-header">
                                <div class="login-logo">
                                    <i class="fas fa-sign-in-alt"></i>
                                </div>
                                <h2 class="login-title">欢迎回来</h2>
                                <p class="login-subtitle">登录您的YOLO检测账户</p>
                            </div>

                            <!-- 登录表单 -->
                            <form @submit.prevent="submit" class="login-form">
                                <!-- 用户名输入 -->
                                <div class="form-group">
                                    <label for="username" class="form-label">
                                        <i class="fas fa-user me-2"></i>用户名
                                    </label>
                                    <input type="text" id="username" name="username" v-model="form.username"
                                        class="form-control" :class="{ 'is-invalid': errors.username }"
                                        placeholder="请输入用户名" required @blur="validateUsername"
                                        @input="clearError('username')" autocomplete="username" />
                                    <div v-if="errors.username" class="invalid-feedback">
                                        {{ errors.username }}
                                    </div>
                                </div>

                                <!-- 密码输入 -->
                                <div class="form-group">
                                    <label for="password" class="form-label">
                                        <i class="fas fa-lock me-2"></i>密码
                                    </label>
                                    <div class="password-input-wrapper">
                                        <input :type="showPassword ? 'text' : 'password'" id="password" name="password"
                                            v-model="form.password" class="form-control"
                                            :class="{ 'is-invalid': errors.password }" placeholder="请输入密码" required
                                            @blur="validatePassword" @input="clearError('password')"
                                            autocomplete="current-password" />
                                        <button type="button" class="password-toggle" @click="togglePassword">
                                            <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                                        </button>
                                    </div>
                                    <div v-if="errors.password" class="invalid-feedback">
                                        {{ errors.password }}
                                    </div>
                                </div>

                                <!-- 记住我 -->
                                <div class="form-group">
                                    <div class="form-check">
                                        <input type="checkbox" id="remember" v-model="rememberMe"
                                            class="form-check-input" />
                                        <label for="remember" class="form-check-label">
                                            记住我
                                        </label>
                                    </div>
                                </div>

                                <!-- 全局错误提示 -->
                                <div v-if="globalError" class="alert alert-danger" role="alert">
                                    <i class="fas fa-exclamation-triangle me-2"></i>
                                    {{ globalError }}
                                </div>

                                <!-- 提交按钮 -->
                                <button type="submit" class="btn btn-primary btn-lg w-100"
                                    :disabled="isLoading || !isFormValid">
                                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                                    <i v-else class="fas fa-sign-in-alt me-2"></i>
                                    {{ isLoading ? '登录中...' : '登录' }}
                                </button>
                            </form>

                            <!-- 底部链接 -->
                            <div class="login-footer">
                                <p class="text-center">
                                    还没有账户？
                                    <router-link to="/register" class="register-link">
                                        立即注册
                                    </router-link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
    name: 'LoginView',
    setup() {
        const store = useStore()
        const router = useRouter()

        // 表单数据
        const form = reactive({
            username: '',
            password: ''
        })

        // 表单验证错误
        const errors = reactive({
            username: '',
            password: ''
        })

        // 组件状态
        const isLoading = ref(false)
        const showPassword = ref(false)
        const rememberMe = ref(false)
        const globalError = ref('')

        // 表单验证规则
        const validateUsername = () => {
            if (!form.username) {
                errors.username = '请输入用户名'
                return false
            }
            if (form.username.length < 3) {
                errors.username = '用户名至少需要3个字符'
                return false
            }
            if (!/^[a-zA-Z0-9_-]+$/.test(form.username)) {
                errors.username = '用户名只能包含字母、数字、下划线和短横线'
                return false
            }
            errors.username = ''
            return true
        }

        const validatePassword = () => {
            if (!form.password) {
                errors.password = '请输入密码'
                return false
            }
            if (form.password.length < 6) {
                errors.password = '密码至少需要6个字符'
                return false
            }
            errors.password = ''
            return true
        }

        // 计算属性
        const isFormValid = computed(() => {
            return form.username &&
                form.password &&
                !errors.username &&
                !errors.password
        })

        // 方法
        const clearError = (field) => {
            errors[field] = ''
            globalError.value = ''
        }

        const togglePassword = () => {
            showPassword.value = !showPassword.value
        }

        const validateForm = () => {
            const isUsernameValid = validateUsername()
            const isPasswordValid = validatePassword()
            return isUsernameValid && isPasswordValid
        }

        const submit = async () => {
            // 清除之前的错误
            globalError.value = ''

            // 验证表单
            if (!validateForm()) {
                return
            }

            try {
                isLoading.value = true

                // 调用Vuex登录action
                await store.dispatch('user/login', {
                    username: form.username,
                    password: form.password,
                    remember: rememberMe.value
                })

                // 登录成功后跳转
                const redirectPath = router.currentRoute.value.query.redirect || '/'
                await router.push(redirectPath)

            } catch (error) {
                console.error('登录失败:', error)

                // 显示错误信息
                if (error.response?.status === 401) {
                    globalError.value = '用户名或密码错误'
                } else if (error.response?.status === 429) {
                    globalError.value = '登录尝试过于频繁，请稍后再试'
                } else if (error.response?.data?.detail) {
                    globalError.value = error.response.data.detail
                } else {
                    globalError.value = '登录失败，请检查网络连接'
                }
            } finally {
                isLoading.value = false
            }
        }

        return {
            form,
            errors,
            isLoading,
            showPassword,
            rememberMe,
            globalError,
            isFormValid,
            clearError,
            togglePassword,
            validateUsername,
            validatePassword,
            submit
        }
    }
}
</script>

<style scoped>
.login-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    padding: 20px 0;
}

.login-wrapper {
    width: 100%;
}

.login-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.login-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

.login-header {
    text-align: center;
    margin-bottom: 30px;
}

.login-logo {
    width: 80px;
    height: 80px;
    margin: 0 auto 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: white;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.login-title {
    color: #333;
    font-weight: 700;
    margin-bottom: 8px;
    font-size: 1.75rem;
}

.login-subtitle {
    color: #666;
    margin-bottom: 0;
    font-size: 0.95rem;
}

.login-form {
    margin-bottom: 25px;
}

.form-group {
    margin-bottom: 20px;
}

.form-label {
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    font-size: 0.9rem;
}

.form-control {
    border: 2px solid #e1e5e9;
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.8);
}

.form-control:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    background: rgba(255, 255, 255, 0.95);
}

.form-control.is-invalid {
    border-color: #dc3545;
}

.password-input-wrapper {
    position: relative;
}

.password-toggle {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: #6c757d;
    cursor: pointer;
    padding: 5px;
    transition: color 0.3s ease;
}

.password-toggle:hover {
    color: #667eea;
}

.form-check {
    margin-bottom: 20px;
}

.form-check-input {
    border-radius: 4px;
    border: 2px solid #e1e5e9;
}

.form-check-input:checked {
    background-color: #667eea;
    border-color: #667eea;
}

.form-check-label {
    color: #666;
    font-size: 0.9rem;
    margin-left: 8px;
}

.alert {
    border-radius: 10px;
    border: none;
    padding: 12px 16px;
    margin-bottom: 20px;
    font-size: 0.9rem;
}

.btn {
    border-radius: 12px;
    font-weight: 600;
    padding: 12px 24px;
    transition: all 0.3s ease;
    border: none;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-size: 1rem;
}

.btn-primary:hover:not(:disabled) {
    background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

.login-footer {
    text-align: center;
    margin-top: 20px;
}

.login-footer p {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0;
}

.register-link {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.3s ease;
}

.register-link:hover {
    color: #5a6fd8;
    text-decoration: underline;
}

.invalid-feedback {
    display: block;
    width: 100%;
    margin-top: 5px;
    font-size: 0.8rem;
    color: #dc3545;
}

.spinner-border-sm {
    width: 1rem;
    height: 1rem;
}

/* 响应式设计 */
@media (max-width: 576px) {
    .login-card {
        padding: 30px 20px;
        margin: 10px;
    }

    .login-title {
        font-size: 1.5rem;
    }

    .login-logo {
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
    }
}

/* 动画效果 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.login-card {
    animation: fadeInUp 0.6s ease-out;
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
    .login-card {
        background: rgba(30, 30, 30, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .login-title {
        color: #fff;
    }

    .login-subtitle {
        color: #ccc;
    }

    .form-label {
        color: #fff;
    }

    .form-control {
        background: rgba(40, 40, 40, 0.8);
        border-color: #555;
        color: #fff;
    }

    .form-control:focus {
        background: rgba(40, 40, 40, 0.95);
    }

    .form-check-label {
        color: #ccc;
    }

    .login-footer p {
        color: #ccc;
    }

    .divider span {
        background: rgba(30, 30, 30, 0.95);
        color: #ccc;
    }
}
</style>