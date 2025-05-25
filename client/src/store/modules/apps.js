import axios from "axios";
import {config} from "@/utils/config.js";

const state = {
    apps: []
};

const getters = {
    APPS: state => state.apps
};

const mutations = {
    SET_APPS(state, payload) {
        state.apps = payload.apps
    }
};

const actions = {
    loadApps: async (context) => {
        await axios.get(config.apiUrl + '/apps', {
            headers: config.headers
        })
            .then((response) => {
                context.commit('SET_APPS', response.data)
            })
    },
    createApp: async (context, payload) => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/apps/create', payload, {
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
    updateApp: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            await axios.put(config.apiUrl + '/apps/update/', payload,{
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