import { createStore } from 'vuex'
import auth from "@/store/modules/auth.js";
import chats from "@/store/modules/chats.js";
import messages from "@/store/modules/messages.js";


const store = createStore({
    modules: {
        auth,
        chats,
        messages
    },
});

export default store;