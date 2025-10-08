<template>
  <header>
    <nav class="navbar navbar-expand-md navbar-dark bg-gradient-dark shadow-lg">
      <div class="container">
        <!-- 品牌Logo -->
        <a class="navbar-brand d-flex align-items-center" href="/">
          <i class="fas fa-robot me-2 brand-icon"></i>
          <span class="brand-text">YOLO Detection</span>
        </a>

        <!-- 移动端切换按钮 -->
        <button class="navbar-toggler border-0" type="button" :class="{ 'collapsed': !isNavbarOpen }"
          @click="toggleNavbar" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- 导航菜单 -->
        <div class="collapse navbar-collapse" :class="{ 'show': isNavbarOpen }" id="navbarCollapse">
          <!-- 已登录用户菜单 -->
          <ul v-if="isLoggedIn" class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link nav-link-custom" to="/" @click="closeNavbar">
                <i class="fas fa-home me-1"></i>
                首页
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link nav-link-custom" to="/dashboard" @click="closeNavbar">
                <i class="fas fa-eye me-1"></i>
                目标检测
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link nav-link-custom" to="/profile" @click="closeNavbar">
                <i class="fas fa-user me-1"></i>
                我的资料
              </router-link>
            </li>
          </ul>

          <!-- 未登录用户菜单 -->
          <ul v-else class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link nav-link-custom" to="/" @click="closeNavbar">
                <i class="fas fa-home me-1"></i>
                首页
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link nav-link-custom" to="/about" @click="closeNavbar">
                <i class="fas fa-info-circle me-1"></i>
                关于
              </router-link>
            </li>
          </ul>

          <!-- 右侧用户操作 -->
          <div class="navbar-nav ms-auto">
            <div v-if="isLoggedIn" class="nav-item dropdown">
              <a class="nav-link dropdown-toggle user-menu" href="#" id="userDropdown" role="button"
                @click="toggleUserMenu" :class="{ 'show': isUserMenuOpen }">
                <i class="fas fa-user-circle me-1"></i>
                <span v-if="currentUser">{{ currentUser }}</span>
                <span v-else>用户</span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end" :class="{ 'show': isUserMenuOpen }">
                <li>
                  <router-link class="dropdown-item" to="/profile" @click="closeMenus">
                    <i class="fas fa-user me-2"></i>个人资料
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/settings" @click="closeMenus">
                    <i class="fas fa-cog me-2"></i>设置
                  </router-link>
                </li>
                <li>
                  <hr class="dropdown-divider">
                </li>
                <li>
                  <a class="dropdown-item text-danger" @click="logout">
                    <i class="fas fa-sign-out-alt me-2"></i>退出登录
                  </a>
                </li>
              </ul>
            </div>

            <!-- 未登录时的按钮 -->
            <div v-else class="d-flex gap-2">
              <router-link class="btn btn-outline-light btn-sm" to="/register" @click="closeNavbar">
                <i class="fas fa-user-plus me-1"></i>注册
              </router-link>
              <router-link class="btn btn-primary btn-sm" to="/login" @click="closeNavbar">
                <i class="fas fa-sign-in-alt me-1"></i>登录
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'NavBar',
  data() {
    return {
      isNavbarOpen: false,
      isUserMenuOpen: false
    };
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters['user/isAuthenticated'];
    },
    currentUser() {
      return this.$store.getters['user/stateUser'];
    }
  },
  methods: {
    async logout() {
      try {
        await this.$store.dispatch('user/logOut');
        this.$router.push('/login');
        this.closeMenus();
      } catch (error) {
        console.error('退出登录失败:', error);
      }
    },

    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
      // 关闭用户菜单
      this.isUserMenuOpen = false;
    },

    toggleUserMenu() {
      this.isUserMenuOpen = !this.isUserMenuOpen;
    },

    closeNavbar() {
      this.isNavbarOpen = false;
    },

    closeMenus() {
      this.isNavbarOpen = false;
      this.isUserMenuOpen = false;
    }
  },

  // 点击外部关闭菜单
  mounted() {
    document.addEventListener('click', (e) => {
      if (!this.$el.contains(e.target)) {
        this.closeMenus();
      }
    });
  }
});
</script>

<style scoped>
/* 自定义渐变背景 */
.bg-gradient-dark {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
}

/* 品牌样式 */
.navbar-brand {
  font-weight: 700;
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.navbar-brand:hover {
  transform: translateY(-2px);
  color: #fff !important;
}

.brand-icon {
  font-size: 1.8rem;
  color: #ffd700;
  animation: pulse 2s infinite;
}

.brand-text {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 导航链接美化 */
.nav-link-custom {
  position: relative;
  padding: 0.8rem 1rem !important;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
  margin: 0 0.2rem;
}

.nav-link-custom:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.nav-link-custom.router-link-active {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700 !important;
  font-weight: 600;
}

.nav-link-custom.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 30px;
  height: 3px;
  background: #ffd700;
  transform: translateX(-50%);
  border-radius: 2px;
}

/* 用户菜单样式 */
.user-menu {
  border-radius: 25px;
  padding: 0.5rem 1rem !important;
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.user-menu:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.dropdown-menu {
  border: none;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  border-radius: 0.8rem;
  padding: 0.5rem 0;
  margin-top: 0.5rem;
}

.dropdown-item {
  padding: 0.7rem 1.5rem;
  transition: all 0.3s ease;
}

.dropdown-item:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: translateX(5px);
}

/* 按钮样式 */
.btn-outline-light {
  border-radius: 20px;
  padding: 0.4rem 1rem;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 255, 255, 0.3);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 20px;
  padding: 0.4rem 1rem;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* 移动端切换按钮 */
.navbar-toggler {
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.navbar-toggler:hover {
  background: rgba(255, 255, 255, 0.1);
}

.navbar-toggler:focus {
  box-shadow: 0 0 0 0.2rem rgba(255, 215, 0, 0.5);
}

/* 阴影效果 */
.shadow-lg {
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175) !important;
}

/* 动画效果 */
@keyframes pulse {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.1);
  }

  100% {
    transform: scale(1);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar-nav {
    padding: 1rem 0;
  }

  .nav-link-custom {
    margin: 0.2rem 0;
    text-align: center;
  }

  .dropdown-menu {
    position: static !important;
    transform: none !important;
    box-shadow: none;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 0.5rem;
  }
}

/* 通用样式 */
a {
  cursor: pointer;
}

/* 图标间距 */
.fas {
  width: 16px;
  text-align: center;
}
</style>