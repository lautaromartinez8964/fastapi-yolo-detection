<template>
    <div class="dashboard-container">
        <div class="dashboard-wrapper">
            <div class="container">
                <!-- 头部标题 -->
                <div class="header-section">
                    <h1 class="dashboard-title">
                        <i class="fas fa-search me-3"></i>
                        YOLO 智能目标检测系统
                    </h1>
                    <p class="dashboard-subtitle">
                        基于深度学习的实时目标检测平台，支持图片和视频分析
                    </p>
                </div>

                <!-- 控制面板 -->
                <div class="control-panel">
                    <!-- 模型选择区域 -->
                    <div class="panel-section">
                        <div class="section-header">
                            <h3 class="section-title">
                                <i class="fas fa-brain me-2"></i>
                                模型配置
                            </h3>
                        </div>
                        <div class="model-controls">
                            <div class="form-group">
                                <label class="form-label">选择YOLO模型</label>
                                <div class="model-selection">
                                    <select v-model="selectedModel" class="form-control model-select"
                                        :disabled="isLoading">
                                        <option value="" disabled>请选择模型</option>
                                        <option v-for="model in availableModels" :key="model" :value="model">
                                            {{ model }}
                                        </option>
                                    </select>
                                    <button type="button" class="btn btn-primary" @click="changeYoloModel"
                                        :disabled="!selectedModel || isLoading">
                                        <i class="fas fa-sync-alt me-2"></i>
                                        {{ isLoading ? '切换中...' : '应用模型' }}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 置信度设置区域 -->
                    <div class="panel-section">
                        <div class="section-header">
                            <h3 class="section-title">
                                <i class="fas fa-sliders-h me-2"></i>
                                检测参数
                            </h3>
                        </div>
                        <div class="confidence-controls">
                            <div class="form-group">
                                <label class="form-label">
                                    置信度阈值: {{ formatPercentage(confThreshold) }}
                                </label>
                                <div class="slider-container">
                                    <span class="slider-label">低</span>
                                    <input type="range" v-model="confThreshold" min="0.1" max="0.9" step="0.05"
                                        class="form-range" />
                                    <span class="slider-label">高</span>
                                </div>
                                <div class="confidence-info">
                                    <small class="text-muted">
                                        <i class="fas fa-info-circle me-1"></i>
                                        较低值会检测更多目标，较高值会提高检测精度
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 检测区域 -->
                <div class="detection-areas">
                    <!-- 图片检测卡片 -->
                    <div class="detection-card">
                        <div class="card-header">
                            <h4 class="card-title">
                                <i class="fas fa-image me-2"></i>
                                图片检测
                            </h4>
                            <p class="card-subtitle">支持JPG、PNG、JPEG格式，可选择多张图片</p>
                        </div>
                        <div class="card-body">
                            <div class="upload-zone" :class="{ 'dragover': isDragging }">
                                <input ref="imageInput" type="file" multiple accept="image/*"
                                    @change="handleImageSelect" class="file-input" />
                                <div class="upload-content" @click="$refs.imageInput.click()">
                                    <i class="fas fa-cloud-upload-alt upload-icon"></i>
                                    <p class="upload-text">点击选择图片或拖拽到此处</p>
                                    <span class="upload-hint">{{ imageFiles.length ? `已选择 ${imageFiles.length} 张图片` :
                                        '支持多张图片同时上传' }}</span>
                                </div>
                            </div>
                            <button type="button" class="btn btn-success btn-lg w-100 mt-3" @click="uploadImages"
                                :disabled="!imageFiles.length || isLoading">
                                <span v-if="isLoading && currentTask === 'image'"
                                    class="spinner-border spinner-border-sm me-2"></span>
                                <i v-else class="fas fa-play me-2"></i>
                                {{ isLoading && currentTask === 'image' ? '检测中...' : '开始图片检测' }}
                            </button>
                        </div>
                    </div>

                    <!-- 视频检测卡片 -->
                    <div class="detection-card">
                        <div class="card-header">
                            <h4 class="card-title">
                                <i class="fas fa-video me-2"></i>
                                视频检测
                            </h4>
                            <p class="card-subtitle">支持MP4、AVI格式，单个视频文件</p>
                        </div>
                        <div class="card-body">
                            <div class="upload-zone" :class="{ 'dragover': isDragging }">
                                <input ref="videoInput" type="file" accept="video/*" @change="handleVideoSelect"
                                    class="file-input" />
                                <div class="upload-content" @click="$refs.videoInput.click()">
                                    <i class="fas fa-cloud-upload-alt upload-icon"></i>
                                    <p class="upload-text">点击选择视频或拖拽到此处</p>
                                    <span class="upload-hint">{{ videoFile ? `已选择: ${videoFile.name}` : '支持单个视频文件上传'
                                        }}</span>
                                </div>
                            </div>
                            <button type="button" class="btn btn-success btn-lg w-100 mt-3" @click="uploadVideo"
                                :disabled="!videoFile || isLoading">
                                <span v-if="isLoading && currentTask === 'video'"
                                    class="spinner-border spinner-border-sm me-2"></span>
                                <i v-else class="fas fa-play me-2"></i>
                                {{ isLoading && currentTask === 'video' ? '检测中...' : '开始视频检测' }}
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 图片检测结果 -->
                <div v-if="resultImages.length" class="results-section">
                    <div class="results-header">
                        <h3 class="results-title">
                            <i class="fas fa-chart-line me-2"></i>
                            图片检测结果
                        </h3>
                        <button type="button" class="btn btn-outline-secondary btn-sm" @click="clearImageResults">
                            <i class="fas fa-trash me-1"></i>
                            清除结果
                        </button>
                    </div>
                    <div class="results-grid">
                        <div v-for="(image, index) in resultImages" :key="index" class="result-item">
                            <div class="comparison-container">
                                <div class="image-container">
                                    <h5 class="image-title">原图</h5>
                                    <div class="image-wrapper">
                                        <img :src="originalImages[index]" :alt="`原图 ${index + 1}`" class="result-image"
                                            @error="handleImageError" @click="previewImage(originalImages[index])" />
                                    </div>
                                </div>
                                <div class="arrow-container">
                                    <i class="fas fa-arrow-right"></i>
                                </div>
                                <div class="image-container">
                                    <h5 class="image-title">检测结果</h5>
                                    <div class="image-wrapper">
                                        <img :src="image" :alt="`检测结果 ${index + 1}`" class="result-image"
                                            @error="handleImageError" @click="previewImage(image)" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 视频检测结果 -->
                <div v-if="resultVideo" class="results-section">
                    <div class="results-header">
                        <h3 class="results-title">
                            <i class="fas fa-film me-2"></i>
                            视频检测结果
                        </h3>
                        <button type="button" class="btn btn-outline-secondary btn-sm" @click="clearVideoResults">
                            <i class="fas fa-trash me-1"></i>
                            清除结果
                        </button>
                    </div>
                    <div class="video-comparison">
                        <div class="video-container">
                            <h5 class="video-title">原视频</h5>
                            <video controls :src="originalVideo" class="result-video" @error="handleVideoError">
                                您的浏览器不支持视频播放
                            </video>
                        </div>
                        <div class="arrow-container">
                            <i class="fas fa-arrow-right"></i>
                        </div>
                        <div class="video-container">
                            <h5 class="video-title">检测结果</h5>
                            <video controls :src="resultVideo" class="result-video" @error="handleVideoError">
                                您的浏览器不支持视频播放
                            </video>
                        </div>
                    </div>
                </div>

                <!-- 全局错误提示 -->
                <div v-if="error" class="alert alert-danger mt-4" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    {{ error }}
                    <button type="button" class="btn-close" @click="clearError" aria-label="关闭"></button>
                </div>
            </div>
        </div>

        <!-- 图片预览模态框 -->
        <div v-if="previewImageUrl" class="modal-overlay" @click="closePreview">
            <div class="modal-content" @click.stop>
                <button class="modal-close" @click="closePreview">
                    <i class="fas fa-times"></i>
                </button>
                <img :src="previewImageUrl" alt="预览图片" class="preview-image" />
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'

export default {
    name: 'DashboardView',
    setup() {
        const store = useStore()

        // 响应式数据
        const imageFiles = ref([])
        const videoFile = ref(null)
        const confThreshold = ref(0.25)
        const resultImages = ref([])
        const resultVideo = ref('')
        const originalImages = ref([])
        const originalVideo = ref('')
        const selectedModel = ref('')
        const isDragging = ref(false)
        const currentTask = ref('')
        const previewImageUrl = ref('')

        // 计算属性
        const availableModels = computed(() => store.getters['yolo/availableModels'])
        const isLoading = computed(() => store.getters['yolo/isLoading'])
        const error = computed(() => store.getters['yolo/error'])

        // 方法
        const formatPercentage = (value) => {
            return `${Math.round(value * 100)}%`
        }

        const buildResourceUrl = (baseUrl, path, filename) => {
            const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl
            const cleanPath = path.startsWith('/') ? path : `/${path}`
            return `${cleanBaseUrl}${cleanPath}/${filename}?t=${Date.now()}`
        }

        const showSuccess = (message) => {
            console.log('Success:', message)
            // 这里可以添加成功消息显示逻辑
        }

        const showError = (message) => {
            console.error('Error:', message)
            // 错误信息已通过computed属性显示
        }

        const showWarning = (message) => {
            console.warn('Warning:', message)
            // 这里可以添加警告消息显示逻辑
        }

        const showInfo = (message) => {
            console.info('Info:', message)
            // 这里可以添加信息消息显示逻辑
        }

        // 初始化
        onMounted(async () => {
            try {
                const response = await store.dispatch('yolo/getAvailableModels')
                if (response.current_model) {
                    selectedModel.value = response.current_model
                }
            } catch (error) {
                showError('获取模型列表失败')
            }
        })

        // 文件处理
        const handleImageSelect = (event) => {
            const files = Array.from(event.target.files)
            const validFiles = files.filter(file => {
                if (file.type.startsWith('image/')) {
                    return true
                } else {
                    showWarning(`文件 ${file.name} 不是有效的图片格式`)
                    return false
                }
            })

            if (validFiles.length) {
                imageFiles.value = validFiles
                showInfo(`已选择 ${validFiles.length} 张图片`)
            }
        }

        const handleVideoSelect = (event) => {
            const file = event.target.files[0]
            if (file) {
                if (file.type.startsWith('video/')) {
                    videoFile.value = file
                    showInfo(`已选择视频: ${file.name}`)
                } else {
                    showWarning('请选择有效的视频文件')
                }
            }
        }

        const handleImageError = (e) => {
            console.error('图片加载失败:', e.target.src)
            showWarning('图片加载失败，请检查网络连接')
        }

        const handleVideoError = (e) => {
            console.error('视频加载失败:', e.target.src)
            showWarning('视频加载失败，请检查网络连接')
        }

        // 检测功能
        const uploadImages = async () => {
            if (!imageFiles.value.length) {
                showWarning('请先选择图片')
                return
            }

            try {
                currentTask.value = 'image'
                resultImages.value = []
                originalImages.value = []

                showInfo('正在处理图片，请等候...')

                // 保存原始图片URL
                originalImages.value = imageFiles.value.map(file => URL.createObjectURL(file))

                const response = await store.dispatch('yolo/detectImages', {
                    files: imageFiles.value,
                    confThreshold: confThreshold.value
                })

                const baseUrl = axios.defaults.baseURL || ''
                resultImages.value = response.output_images.map(img =>
                    buildResourceUrl(baseUrl, 'static/outputs/images', img)
                )

                showSuccess('图片检测完成')
            } catch (error) {
                showError('图片检测失败')
            } finally {
                currentTask.value = ''
            }
        }

        const uploadVideo = async () => {
            if (!videoFile.value) {
                showWarning('请先选择视频')
                return
            }

            try {
                currentTask.value = 'video'
                resultVideo.value = ''
                originalVideo.value = ''

                showInfo('正在处理视频，这可能需要一些时间...')

                // 保存原始视频URL
                originalVideo.value = URL.createObjectURL(videoFile.value)

                const response = await store.dispatch('yolo/detectVideo', {
                    file: videoFile.value,
                    confThreshold: confThreshold.value
                })

                const baseUrl = axios.defaults.baseURL || ''
                resultVideo.value = buildResourceUrl(baseUrl, 'static/outputs/videos', response.output_video)

                showSuccess('视频检测完成')
            } catch (error) {
                showError('视频检测失败')
            } finally {
                currentTask.value = ''
            }
        }

        const changeYoloModel = async () => {
            if (!selectedModel.value) {
                showWarning('请选择一个模型')
                return
            }

            try {
                showInfo('正在切换模型...')
                await store.dispatch('yolo/changeModel', selectedModel.value)
                showSuccess(`模型切换成功: ${selectedModel.value}`)
            } catch (error) {
                showError('模型切换失败')
            }
        }

        // 清除结果
        const clearImageResults = () => {
            resultImages.value = []
            originalImages.value = []
            imageFiles.value = []
            // 清空input
            if (document.querySelector('input[type="file"][multiple]')) {
                document.querySelector('input[type="file"][multiple]').value = ''
            }
        }

        const clearVideoResults = () => {
            resultVideo.value = ''
            originalVideo.value = ''
            videoFile.value = null
            // 清空input
            if (document.querySelector('input[type="file"]:not([multiple])')) {
                document.querySelector('input[type="file"]:not([multiple])').value = ''
            }
        }

        const clearError = () => {
            store.commit('yolo/setError', null)
        }

        // 图片预览
        const previewImage = (url) => {
            previewImageUrl.value = url
        }

        const closePreview = () => {
            previewImageUrl.value = ''
        }

        return {
            // 数据
            imageFiles,
            videoFile,
            confThreshold,
            resultImages,
            resultVideo,
            originalImages,
            originalVideo,
            selectedModel,
            isDragging,
            currentTask,
            previewImageUrl,

            // 计算属性
            availableModels,
            isLoading,
            error,

            // 方法
            formatPercentage,
            handleImageSelect,
            handleVideoSelect,
            handleImageError,
            handleVideoError,
            uploadImages,
            uploadVideo,
            changeYoloModel,
            clearImageResults,
            clearVideoResults,
            clearError,
            previewImage,
            closePreview
        }
    }
}
</script>

<style scoped>
.dashboard-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px 0;
}

.dashboard-wrapper {
    width: 100%;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* 头部区域 */
.header-section {
    text-align: center;
    margin-bottom: 40px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.dashboard-title {
    color: #333;
    font-weight: 700;
    margin-bottom: 15px;
    font-size: 2.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.dashboard-subtitle {
    color: #666;
    font-size: 1.1rem;
    margin-bottom: 0;
    line-height: 1.6;
}

/* 控制面板 */
.control-panel {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.panel-section {
    margin-bottom: 30px;
}

.panel-section:last-child {
    margin-bottom: 0;
}

.section-header {
    margin-bottom: 20px;
}

.section-title {
    color: #333;
    font-weight: 600;
    font-size: 1.25rem;
    margin-bottom: 0;
}

/* 表单控件 */
.form-group {
    margin-bottom: 20px;
}

.form-label {
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
    display: block;
    font-size: 0.95rem;
}

.form-control {
    border: 2px solid #e1e5e9;
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.8);
    width: 100%;
}

.form-control:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    background: rgba(255, 255, 255, 0.95);
    outline: none;
}

.form-control:disabled {
    background-color: #f8f9fa;
    opacity: 0.6;
}

/* 模型选择 */
.model-selection {
    display: flex;
    gap: 15px;
    align-items: flex-end;
}

.model-select {
    flex: 1;
    max-width: 300px;
}

/* 置信度滑块 */
.slider-container {
    display: flex;
    align-items: center;
    gap: 15px;
    margin: 10px 0;
}

.form-range {
    flex: 1;
    height: 6px;
    background: #e1e5e9;
    border-radius: 3px;
    outline: none;
    -webkit-appearance: none;
    appearance: none;
}

.form-range::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}

.form-range::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    cursor: pointer;
    border: none;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}

.slider-label {
    font-size: 0.9rem;
    color: #666;
    font-weight: 500;
    min-width: 30px;
    text-align: center;
}

.confidence-info {
    margin-top: 8px;
}

/* 检测区域 */
.detection-areas {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-bottom: 30px;
}

.detection-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.detection-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

.card-header {
    margin-bottom: 20px;
}

.card-title {
    color: #333;
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 5px;
}

.card-subtitle {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0;
}

/* 上传区域 */
.upload-zone {
    border: 2px dashed #e1e5e9;
    border-radius: 15px;
    padding: 30px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    background: rgba(248, 249, 250, 0.5);
}

.upload-zone:hover {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.05);
}

.upload-zone.dragover {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.1);
}

.file-input {
    display: none;
}

.upload-content {
    cursor: pointer;
}

.upload-icon {
    font-size: 3rem;
    color: #667eea;
    margin-bottom: 15px;
    display: block;
}

.upload-text {
    font-size: 1.1rem;
    color: #333;
    margin-bottom: 8px;
    font-weight: 500;
}

.upload-hint {
    color: #666;
    font-size: 0.9rem;
}

/* 按钮样式 */
.btn {
    border-radius: 12px;
    font-weight: 600;
    padding: 12px 24px;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
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

.btn-success {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    color: white;
}

.btn-success:hover:not(:disabled) {
    background: linear-gradient(135deg, #218838 0%, #1ba085 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
}

.btn-outline-secondary {
    border: 2px solid #6c757d;
    color: #6c757d;
    background: transparent;
}

.btn-outline-secondary:hover {
    background: #6c757d;
    color: white;
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

.btn-sm {
    padding: 8px 16px;
    font-size: 0.9rem;
}

/* 结果区域 */
.results-section {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 2px solid #e1e5e9;
}

.results-title {
    color: #333;
    font-weight: 600;
    font-size: 1.3rem;
    margin-bottom: 0;
}

/* 图片结果网格 */
.results-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 30px;
}

.result-item {
    border: 1px solid #e1e5e9;
    border-radius: 15px;
    padding: 20px;
    background: rgba(248, 249, 250, 0.5);
}

.comparison-container {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 20px;
    align-items: center;
}

.image-container {
    text-align: center;
}

.image-title {
    color: #333;
    font-weight: 600;
    margin-bottom: 15px;
    font-size: 1rem;
}

.image-wrapper {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    cursor: pointer;
}

.image-wrapper:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.result-image {
    width: 100%;
    height: auto;
    max-height: 300px;
    object-fit: contain;
    display: block;
}

.arrow-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.arrow-container i {
    font-size: 1.5rem;
    color: #667eea;
}

/* 视频对比 */
.video-comparison {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 20px;
    align-items: center;
}

.video-container {
    text-align: center;
}

.video-title {
    color: #333;
    font-weight: 600;
    margin-bottom: 15px;
    font-size: 1rem;
}

.result-video {
    width: 100%;
    max-height: 400px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

/* 错误提示 */
.alert {
    border-radius: 12px;
    border: none;
    padding: 15px 20px;
    position: relative;
}

.alert-danger {
    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
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

/* 图片预览模态框 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    backdrop-filter: blur(5px);
}

.modal-content {
    position: relative;
    max-width: 90%;
    max-height: 90%;
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
}

.modal-close {
    position: absolute;
    top: 15px;
    right: 15px;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    transition: all 0.3s ease;
}

.modal-close:hover {
    background: rgba(0, 0, 0, 0.7);
}

.preview-image {
    width: 100%;
    height: auto;
    max-width: 100%;
    max-height: calc(90vh - 40px);
    object-fit: contain;
    border-radius: 10px;
}

/* 响应式设计 */
@media (max-width: 992px) {
    .detection-areas {
        grid-template-columns: 1fr;
    }

    .comparison-container,
    .video-comparison {
        grid-template-columns: 1fr;
        gap: 15px;
    }

    .arrow-container {
        transform: rotate(90deg);
    }

    .model-selection {
        flex-direction: column;
        align-items: stretch;
    }

    .model-select {
        max-width: none;
        margin-bottom: 15px;
    }
}

@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }

    .dashboard-title {
        font-size: 2rem;
    }

    .header-section,
    .control-panel,
    .detection-card,
    .results-section {
        padding: 20px;
    }

    .results-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }

    .upload-zone {
        padding: 20px 15px;
    }

    .upload-icon {
        font-size: 2.5rem;
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
.control-panel,
.detection-card,
.results-section {
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
    .control-panel,
    .detection-card,
    .results-section {
        background: rgba(30, 30, 30, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .dashboard-title,
    .section-title,
    .card-title,
    .results-title,
    .image-title,
    .video-title {
        color: #fff;
    }

    .dashboard-subtitle,
    .card-subtitle {
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

    .upload-zone {
        background: rgba(40, 40, 40, 0.5);
        border-color: #555;
    }

    .upload-zone:hover {
        background: rgba(102, 126, 234, 0.1);
    }

    .result-item {
        background: rgba(40, 40, 40, 0.5);
        border-color: #555;
    }
}
</style>