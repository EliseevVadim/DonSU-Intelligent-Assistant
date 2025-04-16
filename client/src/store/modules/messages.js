import axios from "axios";
import {config} from "@/config/config.js";

const state = {
    messages: []
};

const getters = {
    MESSAGES: state => state.messages
};

const mutations = {
    SET_MESSAGES(state, payload) {
        state.messages = payload.messages
    }
};

const actions = {
    loadMessagesByChat: async (context, id) => {
        await axios.get(config.apiUrl + '/messages/' + id, {
            headers: config.headers
        })
            .then((response) => {
                context.commit('SET_MESSAGES', response.data)
            })
    },
    sendMessage: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/messages/send', payload, {
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