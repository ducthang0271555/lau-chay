import axiosClient from "./axiosClient";

const userApi = {
    login: (passcode) => {
        const url = '/users/';
        return axiosClient.post(url, {passcode});
    },

    getAll: () => {
        const url = '/users/';
        return axiosClient.get(url);
    },

    register: (data) => {
        const url = '/users/register';
        return axiosClient.post(url, data);
    }
};

export default userApi;