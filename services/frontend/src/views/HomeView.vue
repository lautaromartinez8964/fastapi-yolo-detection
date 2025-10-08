<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row align-items-center min-vh-75">
          <div class="col-lg-6">
            <div class="hero-content">
              <h1 class="hero-title">
                <span class="gradient-text">YOLO</span>
                目标检测平台
              </h1>
              <p class="hero-subtitle">
                基于最先进的深度学习技术，提供快速、准确的目标检测服务。
                支持图片和视频检测，让AI为你的项目赋能。
              </p>

              <!-- 未登录状态 -->
              <div v-if="!isLoggedIn" class="hero-actions">
                <router-link to="/register" class="btn btn-primary btn-lg me-3">
                  <i class="fas fa-rocket me-2"></i>
                  开始体验
                </router-link>
                <router-link to="/login" class="btn btn-outline-light btn-lg">
                  <i class="fas fa-sign-in-alt me-2"></i>
                  登录
                </router-link>
              </div>

              <!-- 已登录状态 -->
              <div v-else class="hero-actions">
                <router-link to="/dashboard" class="btn btn-success btn-lg me-3">
                  <i class="fas fa-tachometer-alt me-2"></i>
                  进入仪表板
                </router-link>
                <router-link to="/detection" class="btn btn-outline-light btn-lg">
                  <i class="fas fa-eye me-2"></i>
                  开始检测
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="hero-visual">
              <div class="detection-demo">
                <div class="demo-card">
                  <div class="demo-header">
                    <span class="demo-status">
                      <i class="fas fa-circle text-success"></i>
                      实时检测
                    </span>
                  </div>
                  <div class="demo-content">
                    <img src="../assets/logo.png" alt="YOLO Demo" class="demo-image">
                    <div class="detection-overlay">
                      <div class="bbox bbox-1">
                        <span class="bbox-label">汽车 98%</span>
                      </div>
                      <div class="bbox bbox-2">
                        <span class="bbox-label">人 95%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <div class="row">
          <div class="col-12 text-center mb-5">
            <h2 class="section-title">强大功能</h2>
            <p class="section-subtitle">一站式目标检测解决方案</p>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-image"></i>
              </div>
              <h4>图片检测</h4>
              <p>支持多种图片格式，快速识别图片中的目标对象，准确率高达99%</p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-video"></i>
              </div>
              <h4>视频检测</h4>
              <p>实时视频流检测，支持本地视频文件和网络摄像头输入</p>
            </div>
          </div>

          <div class="col-md-4">
            <div class="feature-card">
              <div class="feature-icon">
                <i class="fas fa-cogs"></i>
              </div>
              <h4>多模型支持</h4>
              <p>内置多种YOLO模型，可根据需求灵活切换，平衡速度与精度</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="container">
        <div class="row text-center">
          <div class="col-md-3 col-6">
            <div class="stat-item">
              <div class="stat-number">99%</div>
              <div class="stat-label">检测准确率</div>
            </div>
          </div>
          <div class="col-md-3 col-6">
            <div class="stat-item">
              <div class="stat-number">&lt;100ms</div>
              <div class="stat-label">响应时间</div>
            </div>
          </div>
          <div class="col-md-3 col-6">
            <div class="stat-item">
              <div class="stat-number">80+</div>
              <div class="stat-label">支持类别</div>
            </div>
          </div>
          <div class="col-md-3 col-6">
            <div class="stat-item">
              <div class="stat-number">24/7</div>
              <div class="stat-label">在线服务</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8 text-center">
            <h2 class="cta-title">准备开始了吗？</h2>
            <p class="cta-subtitle">立即体验先进的目标检测技术</p>
            <div class="cta-actions" v-if="!isLoggedIn">
              <router-link to="/register" class="btn btn-primary btn-lg me-3">
                <i class="fas fa-user-plus me-2"></i>
                免费注册
              </router-link>
              <router-link to="/about" class="btn btn-outline-primary btn-lg">
                <i class="fas fa-info-circle me-2"></i>
                了解更多
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomeView',
  computed: {
    isLoggedIn() {
      return this.$store.getters['user/isAuthenticated'];
    },
    currentUser() {
      return this.$store.getters['user/stateUser'];
    }
  },
  mounted() {
    // 页面加载时的动画效果
    this.animateOnScroll();
  },
  methods: {
    animateOnScroll() {
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
          }
        });
      }, observerOptions);

      // 观察需要动画的元素
      document.querySelectorAll('.feature-card, .stat-item').forEach(el => {
        observer.observe(el);
      });
    }
  }
});
</script>

<style scoped>
/* 全局样式 */
.home-container {
  overflow-x: hidden;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
  color: white;
  padding: 100px 0;
  position: relative;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="white" opacity="0.1"/><circle cx="80" cy="40" r="1" fill="white" opacity="0.1"/><circle cx="40" cy="80" r="1.5" fill="white" opacity="0.1"/></svg>');
  animation: float 20s ease-in-out infinite;
}

.min-vh-75 {
  min-height: 75vh;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.gradient-text {
  background: linear-gradient(45deg, #ffd700, #ffed4e, #fff200);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: glow 2s ease-in-out infinite alternate;
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
  line-height: 1.6;
}

.hero-actions .btn {
  padding: 1rem 2rem;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.hero-actions .btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

/* Hero Visual */
.hero-visual {
  position: relative;
  z-index: 2;
}

.detection-demo {
  max-width: 400px;
  margin: 0 auto;
}

.demo-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  transform: rotateY(-10deg) rotateX(5deg);
  transition: transform 0.3s ease;
}

.demo-card:hover {
  transform: rotateY(0deg) rotateX(0deg);
}

.demo-header {
  background: #f8f9fa;
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.demo-status {
  font-size: 0.9rem;
  font-weight: 600;
  color: #28a745;
}

.demo-content {
  position: relative;
  padding: 1rem;
}

.demo-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
}

.detection-overlay {
  position: absolute;
  top: 1rem;
  left: 1rem;
  right: 1rem;
  bottom: 1rem;
  pointer-events: none;
}

.bbox {
  position: absolute;
  border: 2px solid #ff6b6b;
  border-radius: 4px;
  background: rgba(255, 107, 107, 0.1);
}

.bbox-1 {
  top: 20%;
  left: 10%;
  width: 40%;
  height: 30%;
  animation: pulse-box 2s ease-in-out infinite;
}

.bbox-2 {
  top: 50%;
  right: 15%;
  width: 25%;
  height: 35%;
  animation: pulse-box 2s ease-in-out infinite 0.5s;
}

.bbox-label {
  position: absolute;
  top: -25px;
  left: 0;
  background: #ff6b6b;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

/* Features Section */
.features-section {
  padding: 100px 0;
  background: #f8f9fa;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  margin-bottom: 3rem;
}

.feature-card {
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 20px;
  text-align: center;
  height: 100%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(30px);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.feature-card.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: white;
  font-size: 2rem;
}

.feature-card h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-weight: 600;
}

.feature-card p {
  color: #6c757d;
  line-height: 1.6;
  margin: 0;
}

/* Stats Section */
.stats-section {
  padding: 80px 0;
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: white;
}

.stat-item {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
}

.stat-item.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: #ffd700;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* CTA Section */
.cta-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.cta-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-actions .btn {
  padding: 1rem 2rem;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
}

/* 动画效果 */
@keyframes float {

  0%,
  100% {
    transform: translateY(0px);
  }

  50% {
    transform: translateY(-20px);
  }
}

@keyframes glow {
  from {
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
  }

  to {
    text-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
  }
}

@keyframes pulse-box {

  0%,
  100% {
    border-color: #ff6b6b;
    box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.4);
  }

  50% {
    border-color: #ff8e8e;
    box-shadow: 0 0 0 10px rgba(255, 107, 107, 0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .hero-actions .btn {
    display: block;
    margin: 0.5rem auto;
    width: 100%;
    max-width: 300px;
  }

  .demo-card {
    transform: none;
  }

  .section-title {
    font-size: 2rem;
  }

  .stat-number {
    font-size: 2.5rem;
  }

  .cta-title {
    font-size: 2rem;
  }

  .feature-card {
    margin-bottom: 2rem;
  }
}

@media (max-width: 576px) {
  .hero-section {
    padding: 60px 0;
  }

  .features-section {
    padding: 60px 0;
  }

  .stats-section {
    padding: 60px 0;
  }

  .cta-section {
    padding: 60px 0;
  }

  .hero-title {
    font-size: 2rem;
  }
}
</style>