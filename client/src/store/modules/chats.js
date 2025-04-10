import axios from "axios";
import {config} from "@/config/config.js";

const state = {
    chats: []
};

const getters = {
    CHATS: state => state.chats
};

const mutations = {
    SET_CHATS(state, payload) {
        state.chats = payload.chats
    }
};

const actions = {
    loadChats: async (context) => {
        await axios.get(config.apiUrl + '/chats', {
            headers: config.headers
        })
            .then((response) => {
                context.commit('SET_CHATS', response.data)
            })
    },
    deleteChat: (context, id) => {
        return new Promise(async (resolve, reject) => {
            await axios.delete(config.apiUrl + '/chats/' + id, {
                headers: config.headers
            })
                .then((response) => {
                    resolve(response);
                })
                .catch((error) => {
                    reject(error);
                })
        })
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
};