<template>
    <div class="profile-container">
        <div class="profile-wrapper">
            <div class="container">
                <!-- 头部区域 -->
                <div class="header-section">
                    <div class="profile-avatar">
                        <i class="fas fa-user-circle"></i>
                    </div>
                    <h1 class="profile-title">个人资料</h1>
                    <p class="profile-subtitle">管理您的账户信息和设置</p>
                </div>

                <!-- 个人信息卡片 -->
                <div class="profile-card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-user me-2"></i>
                            基本信息
                        </h3>
                    </div>

                    <div class="card-body">
                        <!-- 用户信息展示 -->
                        <div v-if="user" class="user-info">
                            <div class="info-grid">
                                <!-- 用户名 -->
                                <div class="info-item">
                                    <label class="info-label">
                                        <i class="fas fa-user me-2"></i>
                                        用户名
                                    </label>
                                    <div class="info-value">
                                        {{ user.username || '未设置' }}
                                    </div>
                                </div>

                                <!-- 全名 -->
                                <div class="info-item">
                                    <label class="info-label">
                                        <i class="fas fa-id-card me-2"></i>
                                        姓名
                                    </label>
                                    <div class="info-value">
                                        {{ user.full_name || '未设置' }}
                                    </div>
                                </div>

                                <!-- 邮箱 -->
                                <div class="info-item">
                                    <label class="info-label">
                                        <i class="fas fa-envelope me-2"></i>
                                        邮箱
                                    </label>
                                    <div class="info-value">
                                        {{ user.email || '未设置' }}
                                    </div>
                                </div>

                                <!-- 注册时间 -->
                                <div class="info-item">
                                    <label class="info-label">
                                        <i class="fas fa-calendar-alt me-2"></i>
                                        注册时间
                                    </label>
                                    <div class="info-value">
                                        {{ formatDate(user.created_at) }}
                                    </div>
                                </div>

                                <!-- 最后登录 -->
                                <div class="info-item">
                                    <label class="info-label">
                                        <i class="fas fa-clock me-2"></i>
                                        最后登录
                                    </label>
                                    <div class="info-value">
                                        {{ formatDate(user.updated_at) }}
                                    </div>
                                </div>

                                <!-- 用户ID -->
                                <div class="info-item">
                                    <label class="info-label">
                                        <i class="fas fa-hashtag me-2"></i>
                                        用户ID
                                    </label>
                                    <div class="info-value">
                                        {{ user.id }}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 加载状态 -->
                        <div v-else-if="isLoading" class="loading-state">
                            <div class="spinner-border text-primary me-3" role="status">
                                <span class="visually-hidden">加载中...</span>
                            </div>
                            <span>正在加载用户信息...</span>
                        </div>

                        <!-- 错误状态 -->
                        <div v-else-if="error" class="error-state">
                            <div class="alert alert-danger" role="alert">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                {{ error }}
                            </div>
                            <button type="button" class="btn btn-outline-primary" @click="loadUserProfile">
                                <i class="fas fa-redo me-2"></i>
                                重新加载
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 操作按钮区域 -->
                <div class="actions-section">
                    <div class="actions-card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-cogs me-2"></i>
                                账户操作
                            </h3>
                        </div>

                        <div class="card-body">
                            <div class="action-buttons">
                                <!-- 编辑资料按钮 -->
                                <button type="button" class="btn btn-primary btn-lg" @click="editProfile"
                                    :disabled="isLoading">
                                    <i class="fas fa-edit me-2"></i>
                                    编辑资料
                                </button>

                                <!-- 修改密码按钮 -->
                                <button type="button" class="btn btn-outline-secondary btn-lg" @click="changePassword"
                                    :disabled="isLoading">
                                    <i class="fas fa-key me-2"></i>
                                    修改密码
                                </button>

                                <!-- 注销登录按钮 -->
                                <button type="button" class="btn btn-outline-warning btn-lg" @click="logoutAccount"
                                    :disabled="isLoading">
                                    <i class="fas fa-sign-out-alt me-2"></i>
                                    注销登录
                                </button>

                                <!-- 删除账户按钮 -->
                                <button type="button" class="btn btn-outline-danger btn-lg"
                                    @click="showDeleteConfirm = true" :disabled="isLoading">
                                    <i class="fas fa-trash-alt me-2"></i>
                                    删除账户
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 使用统计区域 -->
                <div class="stats-section">
                    <div class="stats-card">
                        <div class="card-header">
                            <h3 class="card-title">
                                <i class="fas fa-chart-bar me-2"></i>
                                使用统计
                            </h3>
                        </div>

                        <div class="card-body">
                            <div class="stats-grid">
                                <div class="stat-item">
                                    <div class="stat-icon">
                                        <i class="fas fa-images"></i>
                                    </div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ stats.imagesProcessed || 0 }}</div>
                                        <div class="stat-label">处理图片</div>
                                    </div>
                                </div>

                                <div class="stat-item">
                                    <div class="stat-icon">
                                        <i class="fas fa-video"></i>
                                    </div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ stats.videosProcessed || 0 }}</div>
                                        <div class="stat-label">处理视频</div>
                                    </div>
                                </div>

                                <div class="stat-item">
                                    <div class="stat-icon">
                                        <i class="fas fa-brain"></i>
                                    </div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ stats.detectionsCount || 0 }}</div>
                                        <div class="stat-label">检测目标</div>
                                    </div>
                                </div>

                                <div class="stat-item">
                                    <div class="stat-icon">
                                        <i class="fas fa-clock"></i>
                                    </div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ stats.totalTime || '0h' }}</div>
                                        <div class="stat-label">使用时长</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 全局错误提示 -->
                <div v-if="globalError" class="alert alert-danger mt-4" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    {{ globalError }}
                    <button type="button" class="btn-close" @click="clearError" aria-label="关闭"></button>
                </div>

                <!-- 成功提示 -->
                <div v-if="successMessage" class="alert alert-success mt-4" role="alert">
                    <i class="fas fa-check-circle me-2"></i>
                    {{ successMessage }}
                    <button type="button" class="btn-close" @click="clearSuccess" aria-label="关闭"></button>
                </div>
            </div>
        </div>

        <!-- 删除确认模态框 -->
        <div v-if="showDeleteConfirm" class="modal-overlay" @click="showDeleteConfirm = false">
            <div class="modal-content" @click.stop>
                <div class="modal-header">
                    <h4 class="modal-title">
                        <i class="fas fa-exclamation-triangle text-danger me-2"></i>
                        确认删除账户
                    </h4>
                    <button type="button" class="modal-close" @click="showDeleteConfirm = false">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <p class="mb-3">您确定要删除您的账户吗？此操作将：</p>
                    <ul class="delete-warning-list">
                        <li><i class="fas fa-exclamation-circle text-warning me-2"></i>永久删除您的个人资料</li>
                        <li><i class="fas fa-exclamation-circle text-warning me-2"></i>清除所有检测历史记录</li>
                        <li><i class="fas fa-exclamation-circle text-warning me-2"></i>无法恢复已删除的数据</li>
                    </ul>
                    <div class="confirmation-input">
                        <label class="form-label">请输入您的用户名以确认删除：</label>
                        <input type="text" v-model="deleteConfirmText" class="form-control"
                            :placeholder="user?.username" />
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="showDeleteConfirm = false">
                        取消
                    </button>
                    <button type="button" class="btn btn-danger" @click="confirmDeleteAccount"
                        :disabled="deleteConfirmText !== user?.username || isDeleting">
                        <span v-if="isDeleting" class="spinner-border spinner-border-sm me-2"></span>
                        <i v-else class="fas fa-trash-alt me-2"></i>
                        {{ isDeleting ? '删除中...' : '确认删除' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
    name: 'ProfileView',
    setup() {
        const store = useStore()
        const router = useRouter()

        // 响应式数据
        const isLoading = ref(false)
        const error = ref('')
        const globalError = ref('')
        const successMessage = ref('')
        const showDeleteConfirm = ref(false)
        const deleteConfirmText = ref('')
        const isDeleting = ref(false)
        const stats = ref({
            imagesProcessed: 0,
            videosProcessed: 0,
            detectionsCount: 0,
            totalTime: '0h'
        })

        // 计算属性
        const user = computed(() => store.getters['user/stateUser'])
        const isAuthenticated = computed(() => store.getters['user/isAuthenticated'])

        // 方法
        const formatDate = (dateString) => {
            if (!dateString) return '未知'
            try {
                const date = new Date(dateString)
                return date.toLocaleString('zh-CN', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                })
            } catch (error) {
                return '日期格式错误'
            }
        }

        const showSuccess = (message) => {
            successMessage.value = message
            setTimeout(() => {
                successMessage.value = ''
            }, 5000)
        }

        const showError = (message) => {
            globalError.value = message
        }

        const clearError = () => {
            globalError.value = ''
            error.value = ''
        }

        const clearSuccess = () => {
            successMessage.value = ''
        }

        // 加载用户资料
        const loadUserProfile = async () => {
            try {
                isLoading.value = true
                error.value = ''

                await store.dispatch('user/viewMe')

                // 模拟加载使用统计数据
                // 在实际项目中，这里应该调用专门的统计API
                stats.value = {
                    imagesProcessed: Math.floor(Math.random() * 100),
                    videosProcessed: Math.floor(Math.random() * 20),
                    detectionsCount: Math.floor(Math.random() * 500),
                    totalTime: `${Math.floor(Math.random() * 48)}h`
                }

            } catch (error) {
                console.error('加载用户资料失败:', error)
                this.error = '加载用户资料失败，请重试'
            } finally {
                isLoading.value = false
            }
        }

        // 编辑资料
        const editProfile = () => {
            showSuccess('编辑功能正在开发中...')
            // 实际项目中这里应该导航到编辑页面或打开编辑模态框
            // router.push('/profile/edit')
        }

        // 修改密码
        const changePassword = () => {
            showSuccess('密码修改功能正在开发中...')
            // 实际项目中这里应该导航到密码修改页面
            // router.push('/profile/change-password')
        }

        // 注销登录
        const logoutAccount = async () => {
            try {
                isLoading.value = true
                await store.dispatch('user/logOut')
                showSuccess('已成功注销登录')
                setTimeout(() => {
                    router.push('/')
                }, 1500)
            } catch (error) {
                console.error('注销失败:', error)
                showError('注销失败，请重试')
            } finally {
                isLoading.value = false
            }
        }

        // 确认删除账户
        const confirmDeleteAccount = async () => {
            if (deleteConfirmText.value !== user.value?.username) {
                showError('用户名不匹配，请重新输入')
                return
            }

            try {
                isDeleting.value = true

                // 调用删除用户API
                await store.dispatch('user/deleteUser', user.value.id)

                showSuccess('账户删除成功')

                // 清除本地状态
                await store.dispatch('user/logOut')

                // 延迟跳转到首页
                setTimeout(() => {
                    router.push('/')
                }, 2000)

            } catch (error) {
                console.error('删除账户失败:', error)
                showError('删除账户失败，请重试')
            } finally {
                isDeleting.value = false
                showDeleteConfirm.value = false
                deleteConfirmText.value = ''
            }
        }

        // 生命周期
        onMounted(async () => {
            // 检查用户是否已登录
            if (!isAuthenticated.value) {
                router.push('/login')
                return
            }

            // 如果没有用户信息，则加载
            if (!user.value) {
                await loadUserProfile()
            } else {
                // 如果已有用户信息，只加载统计数据
                stats.value = {
                    imagesProcessed: Math.floor(Math.random() * 100),
                    videosProcessed: Math.floor(Math.random() * 20),
                    detectionsCount: Math.floor(Math.random() * 500),
                    totalTime: `${Math.floor(Math.random() * 48)}h`
                }
            }
        })

        return {
            // 数据
            isLoading,
            error,
            globalError,
            successMessage,
            showDeleteConfirm,
            deleteConfirmText,
            isDeleting,
            stats,

            // 计算属性
            user,
            isAuthenticated,

            // 方法
            formatDate,
            showSuccess,
            showError,
            clearError,
            clearSuccess,
            loadUserProfile,
            editProfile,
            changePassword,
            logoutAccount,
            confirmDeleteAccount
        }
    }
}
</script>

<style scoped>
.profile-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px 0;
}

.profile-wrapper {
    width: 100%;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 20px;
}

/* 头部区域 */
.header-section {
    text-align: center;
    margin-bottom: 30px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.profile-avatar {
    margin-bottom: 20px;
}

.profile-avatar i {
    font-size: 4rem;
    color: #667eea;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.profile-title {
    color: #333;
    font-weight: 700;
    margin-bottom: 10px;
    font-size: 2rem;
}

.profile-subtitle {
    color: #666;
    font-size: 1rem;
    margin-bottom: 0;
}

/* 卡片通用样式 */
.profile-card,
.actions-card,
.stats-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    margin-bottom: 30px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.profile-card:hover,
.actions-card:hover,
.stats-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

.card-header {
    padding: 25px 30px 20px;
    border-bottom: 2px solid #e1e5e9;
}

.card-title {
    color: #333;
    font-weight: 600;
    font-size: 1.3rem;
    margin-bottom: 0;
}

.card-body {
    padding: 25px 30px;
}

/* 用户信息网格 */
.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.info-item {
    padding: 20px;
    background: rgba(248, 249, 250, 0.8);
    border-radius: 15px;
    border: 1px solid #e1e5e9;
    transition: all 0.3s ease;
}

.info-item:hover {
    background: rgba(248, 249, 250, 1);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.info-label {
    font-weight: 600;
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 8px;
    display: block;
}

.info-value {
    color: #333;
    font-size: 1.1rem;
    font-weight: 500;
    word-break: break-word;
}

/* 加载和错误状态 */
.loading-state,
.error-state {
    text-align: center;
    padding: 40px 20px;
}

.loading-state {
    color: #666;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}

.error-state .alert {
    margin-bottom: 20px;
}

/* 操作按钮 */
.action-buttons {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.btn {
    border-radius: 12px;
    font-weight: 600;
    padding: 15px 25px;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    font-size: 1rem;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-outline-secondary {
    border: 2px solid #6c757d;
    color: #6c757d;
    background: transparent;
}

.btn-outline-secondary:hover:not(:disabled) {
    background: #6c757d;
    color: white;
    transform: translateY(-2px);
}

.btn-outline-warning {
    border: 2px solid #ffc107;
    color: #ffc107;
    background: transparent;
}

.btn-outline-warning:hover:not(:disabled) {
    background: #ffc107;
    color: #212529;
    transform: translateY(-2px);
}

.btn-outline-danger {
    border: 2px solid #dc3545;
    color: #dc3545;
    background: transparent;
}

.btn-outline-danger:hover:not(:disabled) {
    background: #dc3545;
    color: white;
    transform: translateY(-2px);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
}

.btn-lg {
    padding: 15px 30px;
    font-size: 1.1rem;
}

/* 统计区域 */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.stat-item {
    display: flex;
    align-items: center;
    padding: 25px 20px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-radius: 15px;
    border: 1px solid rgba(102, 126, 234, 0.2);
    transition: all 0.3s ease;
}

.stat-item:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
}

.stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20px;
}

.stat-icon i {
    font-size: 1.5rem;
    color: white;
}

.stat-content {
    flex: 1;
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #333;
    line-height: 1;
}

.stat-label {
    font-size: 0.9rem;
    color: #666;
    margin-top: 5px;
}

/* 模态框样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    backdrop-filter: blur(5px);
}

.modal-content {
    background: white;
    border-radius: 15px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow: auto;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    position: relative;
}

.modal-header {
    padding: 20px 25px;
    border-bottom: 2px solid #e1e5e9;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-title {
    margin: 0;
    color: #333;
    font-size: 1.2rem;
    font-weight: 600;
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.2rem;
    color: #6c757d;
    cursor: pointer;
    padding: 5px;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.modal-close:hover {
    background: #f8f9fa;
    color: #333;
}

.modal-body {
    padding: 25px;
}

.modal-footer {
    padding: 20px 25px;
    border-top: 2px solid #e1e5e9;
    display: flex;
    justify-content: flex-end;
    gap: 15px;
}

.delete-warning-list {
    list-style: none;
    padding: 0;
    margin: 15px 0;
}

.delete-warning-list li {
    padding: 8px 0;
    color: #dc3545;
}

.confirmation-input {
    margin-top: 20px;
}

.form-label {
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
    display: block;
    font-size: 0.9rem;
}

.form-control {
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    width: 100%;
}

.form-control:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    outline: none;
}

/* 警告和成功提示 */
.alert {
    border-radius: 12px;
    border: none;
    padding: 15px 20px;
    position: relative;
    margin-bottom: 20px;
}

.alert-danger {
    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
    color: white;
}

.alert-success {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    color: white;
}

.btn-close {
    position: absolute;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: inherit;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0;
    width: 20px;
    height: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }

    .profile-title {
        font-size: 1.5rem;
    }

    .header-section,
    .card-header,
    .card-body {
        padding: 20px;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    .action-buttons {
        grid-template-columns: 1fr;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }

    .stat-item {
        padding: 20px 15px;
    }

    .modal-content {
        width: 95%;
        margin: 20px;
    }
}

@media (max-width: 576px) {
    .profile-avatar i {
        font-size: 3rem;
    }

    .stat-number {
        font-size: 1.5rem;
    }

    .stat-icon {
        width: 50px;
        height: 50px;
        margin-right: 15px;
    }

    .stat-icon i {
        font-size: 1.2rem;
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

.header-section,
.profile-card,
.actions-card,
.stats-card {
    animation: fadeInUp 0.6s ease-out;
}

/* 加载动画 */
.spinner-border-sm {
    width: 1rem;
    height: 1rem;
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {

    .header-section,
    .profile-card,
    .actions-card,
    .stats-card,
    .modal-content {
        background: rgba(30, 30, 30, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .profile-title,
    .card-title,
    .info-value,
    .stat-number,
    .modal-title {
        color: #fff;
    }

    .profile-subtitle,
    .info-label,
    .stat-label {
        color: #ccc;
    }

    .form-control {
        background: rgba(40, 40, 40, 0.8);
        border-color: #555;
        color: #fff;
    }

    .form-control:focus {
        background: rgba(40, 40, 40, 0.95);
    }

    .info-item {
        background: rgba(40, 40, 40, 0.8);
        border-color: #555;
    }

    .info-item:hover {
        background: rgba(40, 40, 40, 1);
    }
}
</style>
