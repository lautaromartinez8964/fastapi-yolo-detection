import { createStore } from "vuex";

import user from './modules/user';
import yolo from './modules/yolo';

export default createStore({
    modules: {
        user,
        yolo
    }
});