import { createStore } from 'vuex'
import auth from "@/store/modules/auth.js";
import chats from "@/store/modules/chats.js";


const store = createStore({
    modules: {
        auth,
        chats
    },
});

export default store;