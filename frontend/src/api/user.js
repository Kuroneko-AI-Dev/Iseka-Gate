import api from "./axios";


export async function getProfile(){

    const res = await api.get("/auth/me");

    return res.data;

}