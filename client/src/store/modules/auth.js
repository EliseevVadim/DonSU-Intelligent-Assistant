import axios from "axios";
import {config} from "@/utils/config.js";
import store from "@/store/index.js";

const state = {
    access_token: localStorage.getItem('access_token') || null,
    current_user: null
};

const getters = {
    isAuthenticated: state => !!state.access_token,
    CURRENT_USER: state => state.current_user
};

const mutations = {
    SET_ACCESS_TOKEN(state, token) {
        localStorage.setItem('access_token', token)
        state.access_token = token
        config.headers = {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        };
    },
    REMOVE_ACCESS_TOKEN(state) {
        localStorage.removeItem('access_token')
        state.access_token = null
    },
    SET_CURRENT_USER(state, user_info) {
        state.current_user = user_info
    }
};

const actions = {
    register: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/auth/register', payload)
                .then((response) => {
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    login: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            let formData = new FormData();
            formData.append('username', payload.email);
            formData.append('password', payload.password);
            await axios.post(config.apiUrl + '/auth/login', formData)
                .then((response) => {
                    context.commit('SET_ACCESS_TOKEN', response.data.access_token);
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    authenticateExternally: (context, access_token) => {
        return new Promise((resolve, reject) => {
            try {
                context.commit('SET_ACCESS_TOKEN', access_token);
                resolve();
            }
            catch {
                reject();
            }
        })
    },
    requestPasswordReset: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/auth/password/reset', payload)
                .then((response) => {
                    resolve(response);
                })
                .catch((error) => {
                    reject(error)
                });
        })
    },
    resetPassword: (context, payload) => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/auth/password/reset/confirm', payload)
                .then((response) => {
                    resolve(response);
                })
                .catch((error) => {
                    reject(error)
                });
        })
    },
    logout: (context) => {
        return new Promise(async (resolve, reject) => {
            await axios.post(config.apiUrl + '/auth/logout')
                .then((response) => {
                    context.commit('REMOVE_ACCESS_TOKEN');
                    context.commit('SET_CURRENT_USER', null);
                    resolve(response);
                })
                .catch((error) => {
                    reject(error)
                })
        })
    },
    loadUserInfo: async (context) => {
        await axios.get(config.apiUrl + '/auth/me', {
            headers: config.headers
        })
            .then((response) => {
                context.commit('SET_CURRENT_USER', response.data);
            })
            .catch((error) => {
                console.log(error);
            })
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
};