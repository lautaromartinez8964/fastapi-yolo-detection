<template>
  <div class="register-container">
    <div class="register-wrapper">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-5 col-md-7">
            <!-- 注册卡片 -->
            <div class="register-card">
              <!-- 头部 -->
              <div class="register-header">
                <div class="register-logo">
                  <i class="fas fa-user-plus"></i>
                </div>
                <h2 class="register-title">创建账户</h2>
                <p class="register-subtitle">加入YOLO检测平台</p>
              </div>

              <!-- 注册表单 -->
              <form @submit.prevent="submit" class="register-form">
                <!-- 用户名输入 -->
                <div class="form-group">
                  <label for="username" class="form-label">
                    <i class="fas fa-user me-2"></i>用户名
                  </label>
                  <input
                    type="text"
                    id="username"
                    name="username"
                    v-model="user.username"
                    class="form-control"
                    :class="{ 'is-invalid': errors.username }"
                    placeholder="请输入用户名"
                    required
                    @blur="validateUsername"
                    @input="clearError('username')"
                  />
                  <div v-if="errors.username" class="invalid-feedback">
                    {{ errors.username }}
                  </div>
                </div>

                <!-- 全名输入 -->
                <div class="form-group">
                  <label for="full_name" class="form-label">
                    <i class="fas fa-id-card me-2"></i>真实姓名
                  </label>
                  <input
                    type="text"
                    id="full_name"
                    name="full_name"
                    v-model="user.full_name"
                    class="form-control"
                    :class="{ 'is-invalid': errors.full_name }"
                    placeholder="请输入真实姓名"
                    required
                    @blur="validateFullName"
                    @input="clearError('full_name')"
                  />
                  <div v-if="errors.full_name" class="invalid-feedback">
                    {{ errors.full_name }}
                  </div>
                </div>

                <!-- 密码输入 -->
                <div class="form-group">
                  <label for="password" class="form-label">
                    <i class="fas fa-lock me-2"></i>密码
                  </label>
                  <div class="password-input-wrapper">
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      id="password"
                      name="password"
                      v-model="user.password"
                      class="form-control"
                      :class="{ 'is-invalid': errors.password }"
                      placeholder="请输入密码"
                      required
                      @blur="validatePassword"
                      @input="clearError('password')"
                    />
                    <button
                      type="button"
                      class="password-toggle"
                      @click="togglePassword"
                    >
                      <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                  <div v-if="errors.password" class="invalid-feedback">
                    {{ errors.password }}
                  </div>
                  <div class="password-strength">
                    <div class="strength-meter">
                      <div 
                        class="strength-bar" 
                        :class="passwordStrengthClass"
                        :style="{ width: passwordStrength + '%' }"
                      ></div>
                    </div>
                    <small class="strength-text">{{ passwordStrengthText }}</small>
                  </div>
                </div>

                <!-- 确认密码 -->
                <div class="form-group">
                  <label for="confirmPassword" class="form-label">
                    <i class="fas fa-lock me-2"></i>确认密码
                  </label>
                  <input
                    type="password"
                    id="confirmPassword"
                    name="confirmPassword"
                    v-model="confirmPassword"
                    class="form-control"
                    :class="{ 'is-invalid': errors.confirmPassword }"
                    placeholder="请再次输入密码"
                    required
                    @blur="validateConfirmPassword"
                    @input="clearError('confirmPassword')"
                  />
                  <div v-if="errors.confirmPassword" class="invalid-feedback">
                    {{ errors.confirmPassword }}
                  </div>
                </div>

                <!-- 同意条款 -->
                <div class="form-group">
                  <div class="form-check">
                    <input
                      type="checkbox"
                      id="agreeTerms"
                      v-model="agreeTerms"
                      class="form-check-input"
                      :class="{ 'is-invalid': errors.agreeTerms }"
                      required
                    />
                    <label for="agreeTerms" class="form-check-label">
                      我同意 <a href="/terms" target="_blank">服务条款</a> 和 <a href="/privacy" target="_blank">隐私政策</a>
                    </label>
                    <div v-if="errors.agreeTerms" class="invalid-feedback">
                      {{ errors.agreeTerms }}
                    </div>
                  </div>
                </div>

                <!-- 全局错误提示 -->
                <div v-if="globalError" class="alert alert-danger" role="alert">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  {{ globalError }}
                </div>

                <!-- 提交按钮 -->
                <button
                  type="submit"
                  class="btn btn-primary btn-lg w-100"
                  :disabled="isLoading || !isFormValid"
                >
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="fas fa-user-plus me-2"></i>
                  {{ isLoading ? '创建中...' : '创建账户' }}
                </button>
              </form>

              <!-- 底部链接 -->
              <div class="register-footer">
                <p class="text-center">
                  已有账户？
                  <router-link to="/login" class="login-link">
                    立即登录
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
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'RegisterView',
  data() {
    return {
      user: {
        username: '',
        full_name: '',
        password: '',
      },
      confirmPassword: '',
      agreeTerms: false,
      showPassword: false,
      isLoading: false,
      globalError: '',
      errors: {
        username: '',
        full_name: '',
        password: '',
        confirmPassword: '',
        agreeTerms: ''
      }
    };
  },
  computed: {
    // 表单是否有效
    isFormValid() {
      return (
        this.user.username.length >= 3 &&
        this.user.full_name.length >= 2 &&
        this.user.password.length >= 6 &&
        this.confirmPassword === this.user.password &&
        this.agreeTerms &&
        !Object.values(this.errors).some(error => error)
      );
    },
    
    // 密码强度
    passwordStrength() {
      const password = this.user.password;
      let strength = 0;
      
      if (password.length >= 6) strength += 20;
      if (password.length >= 8) strength += 20;
      if (/[A-Z]/.test(password)) strength += 20;
      if (/[0-9]/.test(password)) strength += 20;
      if (/[^A-Za-z0-9]/.test(password)) strength += 20;
      
      return strength;
    },
    
    passwordStrengthClass() {
      if (this.passwordStrength <= 20) return 'strength-weak';
      if (this.passwordStrength <= 60) return 'strength-medium';
      return 'strength-strong';
    },
    
    passwordStrengthText() {
      if (this.passwordStrength <= 20) return '密码强度：弱';
      if (this.passwordStrength <= 60) return '密码强度：中等';
      return '密码强度：强';
    }
  },
  methods: {
    // 验证用户名
    validateUsername() {
      if (!this.user.username) {
        this.errors.username = '用户名不能为空';
      } else if (this.user.username.length < 3) {
        this.errors.username = '用户名至少需要3个字符';
      } else if (!/^[a-zA-Z0-9_]+$/.test(this.user.username)) {
        this.errors.username = '用户名只能包含字母、数字和下划线';
      } else {
        this.errors.username = '';
      }
    },
    
    // 验证真实姓名
    validateFullName() {
      if (!this.user.full_name) {
        this.errors.full_name = '真实姓名不能为空';
      } else if (this.user.full_name.length < 2) {
        this.errors.full_name = '真实姓名至少需要2个字符';
      } else {
        this.errors.full_name = '';
      }
    },
    
    // 验证密码
    validatePassword() {
      if (!this.user.password) {
        this.errors.password = '密码不能为空';
      } else if (this.user.password.length < 6) {
        this.errors.password = '密码至少需要6个字符';
      } else {
        this.errors.password = '';
      }
      
      // 如果确认密码已经输入，重新验证确认密码
      if (this.confirmPassword) {
        this.validateConfirmPassword();
      }
    },
    
    // 验证确认密码
    validateConfirmPassword() {
      if (!this.confirmPassword) {
        this.errors.confirmPassword = '请确认密码';
      } else if (this.confirmPassword !== this.user.password) {
        this.errors.confirmPassword = '两次输入的密码不一致';
      } else {
        this.errors.confirmPassword = '';
      }
    },
    
    // 清除错误
    clearError(field) {
      this.errors[field] = '';
      this.globalError = '';
    },
    
    // 切换密码显示
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    
    // 验证所有字段
    validateAll() {
      this.validateUsername();
      this.validateFullName();
      this.validatePassword();
      this.validateConfirmPassword();
      
      if (!this.agreeTerms) {
        this.errors.agreeTerms = '请同意服务条款和隐私政策';
      } else {
        this.errors.agreeTerms = '';
      }
    },
    
    // 提交表单
    async submit() {
      // 验证所有字段
      this.validateAll();
      
      // 如果表单无效，不提交
      if (!this.isFormValid) {
        return;
      }
      
      this.isLoading = true;
      this.globalError = '';
      
      try {
        // 调用store中的注册action
        await this.$store.dispatch('user/register', this.user);
        
        // 注册成功，跳转到仪表板
        this.$router.push('/dashboard');
        
        // 显示成功消息
        this.$toast?.success('注册成功！欢迎加入YOLO检测平台！');
        
      } catch (error) {
        console.error('注册失败:', error);
        
        // 处理不同类型的错误
        if (error.response?.status === 400) {
          this.globalError = '用户名已存在，请选择其他用户名';
        } else if (error.response?.status === 422) {
          this.globalError = '输入数据格式不正确，请检查后重试';
        } else {
          this.globalError = '注册失败，请稍后重试';
        }
      } finally {
        this.isLoading = false;
      }
    }
  },
  
  // 组件挂载时的设置
  mounted() {
    // 如果用户已经登录，重定向到仪表板
    if (this.$store.getters['user/isAuthenticated']) {
      this.$router.push('/dashboard');
    }
  }
});
</script>

<style scoped>
/* 注册容器 */
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.register-wrapper {
  width: 100%;
}

/* 注册卡片 */
.register-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  padding: 3rem 2.5rem;
  margin: 2rem 0;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 注册头部 */
.register-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.register-logo {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
  font-size: 2.5rem;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.register-title {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.register-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
}

/* 表单样式 */
.register-form {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
}

.form-label i {
  color: #667eea;
  width: 20px;
}

.form-control {
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
  background: white;
}

.form-control.is-invalid {
  border-color: #dc3545;
  background: #fff5f5;
}

.form-control.is-invalid:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

/* 密码输入容器 */
.password-input-wrapper {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: color 0.3s ease;
}

.password-toggle:hover {
  color: #667eea;
}

/* 密码强度指示器 */
.password-strength {
  margin-top: 0.5rem;
}

.strength-meter {
  width: 100%;
  height: 4px;
  background: #e9ecef;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.25rem;
}

.strength-bar {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 2px;
}

.strength-weak {
  background: #dc3545;
}

.strength-medium {
  background: #ffc107;
}

.strength-strong {
  background: #28a745;
}

.strength-text {
  font-size: 0.875rem;
  color: #6c757d;
}

/* 复选框样式 */
.form-check {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.form-check-input {
  margin-top: 0.25rem;
  border: 2px solid #dee2e6;
  border-radius: 4px;
}

.form-check-input:checked {
  background-color: #667eea;
  border-color: #667eea;
}

.form-check-label {
  font-size: 0.9rem;
  color: #6c757d;
  line-height: 1.5;
}

.form-check-label a {
  color: #667eea;
  text-decoration: none;
}

.form-check-label a:hover {
  text-decoration: underline;
}

/* 错误提示 */
.invalid-feedback {
  display: block;
  width: 100%;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #dc3545;
}

.alert {
  border-radius: 12px;
  margin-bottom: 1.5rem;
  padding: 1rem;
  border: none;
}

.alert-danger {
  background: #fff5f5;
  color: #dc3545;
  border-left: 4px solid #dc3545;
}

/* 提交按钮 */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* 注册页脚 */
.register-footer {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register-card {
    padding: 2rem 1.5rem;
    margin: 1rem;
    border-radius: 16px;
  }
  
  .register-title {
    font-size: 1.75rem;
  }
  
  .register-logo {
    width: 60px;
    height: 60px;
    font-size: 2rem;
  }
  
  .form-control {
    padding: 0.625rem 0.875rem;
  }
  
  .btn-primary {
    padding: 0.875rem 1.5rem;
  }
}

@media (max-width: 576px) {
  .register-container {
    padding: 1rem 0;
  }
  
  .register-card {
    padding: 1.5rem 1rem;
    margin: 0.5rem;
  }
  
  .register-title {
    font-size: 1.5rem;
  }
}

/* 动画效果 */
.form-control:focus,
.btn:focus {
  outline: none;
}

.form-group {
  animation: fadeInUp 0.6s ease-out;
  animation-fill-mode: both;
}

.form-group:nth-child(1) { animation-delay: 0.1s; }
.form-group:nth-child(2) { animation-delay: 0.2s; }
.form-group:nth-child(3) { animation-delay: 0.3s; }
.form-group:nth-child(4) { animation-delay: 0.4s; }
.form-group:nth-child(5) { animation-delay: 0.5s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>