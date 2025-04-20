import axios from "axios";
import {config} from "@/utils/config.js";

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
    createChat: () => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/chats/create', {}, {
                headers: config.headers
            })
                .then((response) => {
                    resolve(response);
                })
                .catch((error) => {
                    reject(error);
                })
        })
    },
    renameChat: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            await axios.put(config.apiUrl + '/chats/rename/', {
                'chat_id': payload.chat_id,
                'new_name': payload.new_name
            },{
                headers: config.headers
            })
                .then((response) => {
                    resolve(response);
                })
                .catch((error) => {
                    reject(error);
                })
        })
    },
    deleteChat: (context, id) => {
        return new Promise(async (resolve, reject) => {
            await axios.delete(config.apiUrl + '/chats/delete/' + id, {
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