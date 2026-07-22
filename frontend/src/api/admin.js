import api from "./axios";

export async function getAdminStats() {

    const res = await api.get("/admin/stats");

    return res.data;

}

export async function getUsers() {

    const res = await api.get("/admin/users");

    return res.data;

}

export async function setPremium(userId, value){

    const res = await api.patch(
        `/admin/user/${userId}/premium`,
        null,
        {
            params:{
                is_premium:value
            }
        }
    );

    return res.data;

}

export async function setBan(userId,value){

    const res = await api.patch(
        `/admin/user/${userId}/ban`,
        null,
        {
            params:{
                is_banned:value
            }
        }
    );

    return res.data;

}

export async function deleteUser(userId){

    const res = await api.delete(
        `/admin/user/${userId}`
    );

    return res.data;

}