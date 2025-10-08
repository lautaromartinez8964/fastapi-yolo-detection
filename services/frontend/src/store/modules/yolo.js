import axios from 'axios';

const API_URL = 'http://localhost:5000/yolo';  // 根据你的 FastAPI 后端地址调整

// 定义状态
const state = {
    // 存储检测结果
    detectionResults: null,
    // 存储可用的模型列表
    availableModels: [],
    // 当前使用的模型
    currentModel: null,
    // 加载状态
    isLoading: false,
    // 错误信息
    error: null
};

// 定义获取器
const getters = {
    // 获取检测结果
    detectionResults: state => state.detectionResults,
    // 获取可用模型列表
    availableModels: state => state.availableModels,
    // 获取当前模型
    currentModel: state => state.currentModel,
    // 获取加载状态
    isLoading: state => state.isLoading,
    // 获取错误信息
    error: state => state.error
};

// 定义动作
const actions = {
    // 1. 获取可用的YOLO模型
    async getAvailableModels({ commit }) {
        commit('setLoading', true);
        commit('setError', null);
        try {
            const response = await axios.get(`${API_URL}/available_models`);
            commit('setAvailableModels', response.data);
            return response.data;
        } catch (error) {
            console.error('获取模型列表失败:', error);
            commit('setError', '获取模型列表失败');
            throw error;
        } finally {
            commit('setLoading', false);
        }
    },

    // 2. 执行图片检测
    async detectImages({ commit }, { files, confThreshold }) {
        commit('setLoading', true);
        commit('setError', null);

        const formData = new FormData();
        files.forEach((file) => {
            formData.append('files', file);
        });
        formData.append('conf_threshold', confThreshold);

        try {
            const response = await axios.post(`${API_URL}/detect_picture`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            commit('setDetectionResults', response.data);
            return response.data;
        } catch (error) {
            console.error('图片检测失败:', error);
            commit('setError', '图片检测失败');
            throw error;
        } finally {
            commit('setLoading', false);
        }
    },

    // 3. 执行视频检测
    async detectVideo({ commit }, { file, confThreshold }) {
        commit('setLoading', true);
        commit('setError', null);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('conf_threshold', confThreshold);

        try {
            const response = await axios.post(`${API_URL}/detect_video`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            commit('setDetectionResults', response.data);
            return response.data;
        } catch (error) {
            console.error('视频检测失败:', error);
            commit('setError', '视频检测失败');
            throw error;
        } finally {
            commit('setLoading', false);
        }
    },

    // 4. 切换YOLO模型
    async changeModel({ commit }, modelPath) {
        commit('setLoading', true);
        commit('setError', null);

        const formData = new FormData();
        formData.append('model_path', modelPath);

        try {
            const response = await axios.post(`${API_URL}/change_model`, formData);
            commit('setCurrentModel', modelPath);
            return response.data;
        } catch (error) {
            console.error('切换模型失败:', error);
            commit('setError', '切换模型失败');
            throw error;
        } finally {
            commit('setLoading', false);
        }
    },

    // 清除检测结果
    clearResults({ commit }) {
        commit('setDetectionResults', null);
        commit('setError', null);
    }
};

// 定义突变
const mutations = {
    // 设置检测结果
    setDetectionResults(state, results) {
        state.detectionResults = results;
    },
    // 设置可用模型列表
    setAvailableModels(state, data) {
        // 处理后端返回的数据格式
        if (data && data.models) {
            state.availableModels = data.models;
            if (data.current_model) {
                state.currentModel = data.current_model;
            }
        } else {
            state.availableModels = data || [];
        }
    },
    // 设置当前模型
    setCurrentModel(state, model) {
        state.currentModel = model;
    },
    // 设置加载状态
    setLoading(state, isLoading) {
        state.isLoading = isLoading;
    },
    // 设置错误信息
    setError(state, error) {
        state.error = error;
    }
};

// 导出 Vuex 模块
export default {
    namespaced: true, // 启用命名空间
    state,
    getters,
    actions,
    mutations
};