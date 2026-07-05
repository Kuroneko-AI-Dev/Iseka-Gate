import api from "./api/axios";
import { API_URL } from "./config";

export async function sendMessage(
  message,
  conversationId,
  voice
){

  const response = await api.post(
    "/chat",
    {
      message,
      conversation_id: conversationId,
      voice,
      style: localStorage.getItem("style")
    }
  );

  return response.data;
}

export async function getConversations(){

    const response = await api.get(
        "/conversations"
    );

    return response.data;
}



export async function getMessages(id){

    const response = await api.get(
        `/conversations/${id}`
    );

    return response.data;
}


export async function renameConversation(id, title){

    const token = localStorage.getItem("token");

    const res = await fetch(

        `${API_URL}/conversations/${id}`,

        {

            method:"PUT",

            headers:{

                "Content-Type":"application/json",

                Authorization:`Bearer ${token}`

            },

            body:JSON.stringify({

                title

            })

        }

    );

    return await res.json();

}

export async function deleteConversation(id){

    const token = localStorage.getItem("token");

    const res = await fetch(

        `${API_URL}/conversations/${id}`,

        {

            method:"DELETE",

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    );

    return await res.json();

}