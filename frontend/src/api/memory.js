import api from "./axios";

export async function getMemories() {

    const res = await api.get("/memories");

    return res.data;

}

export async function createMemory(memory_key, memory_value){

    const res = await api.post("/memories",{

        memory_key,

        memory_value

    });

    return res.data;

}

export async function updateMemory(id,memory_key,memory_value){

    const res = await api.put(`/memories/${id}`,{

        memory_key,

        memory_value

    });

    return res.data;

}

export async function deleteMemory(id){

    const res = await api.delete(`/memories/${id}`);

    return res.data;

}

export async function deleteAllMemories(){

    const res = await api.delete("/memories");

    return res.data;

}