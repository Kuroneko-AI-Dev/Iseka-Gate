import api from "./api/axios";
import { API_URL } from "./config";

export async function sendMessage(
  message,
  conversationId,
  voice,
  vision = null
){

  const response = await api.post(
    "/chat",
    {
      message,
      conversation_id: conversationId,
      voice,
      style: localStorage.getItem("style"),
      vision
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

export async function activatePremium() {

  const response = await api.post(
    "/premium/activate"
  );

  return response.data;

}

export async function getPremiumStatus() {

  const response = await api.get(
    "/premium/status"
  );

  return response.data;

}

export async function createPayment(plan){

    const token = localStorage.getItem("token");

    const res = await fetch(
        `${API_URL}/payment/create`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                Authorization:`Bearer ${token}`
            },
            body:JSON.stringify({
                plan
            })
        }
    );

    return res.json();
}

export async function translateText(text){

    const response = await fetch(
        `${API_URL}/translate`,
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json",
                "Authorization":
                `Bearer ${localStorage.getItem("token")}`
            },

            body:JSON.stringify({
                text:text
            })
        }
    );


    return await response.json();

}

export async function researchWeb(query){
    const response = await api.post("/research", {
        query,
        max_results: 5
    });
    return response.data;
}



export async function speechToText(audioBlob){

    const formData = new FormData();

    formData.append(
        "file",
        audioBlob,
        "recording.wav"
    );


    const response = await api.post(
        "/stt",
        formData,
        {
            headers:{
                "Content-Type":"multipart/form-data"
            }
        }
    );


    return response.data;

}


export async function analyzeVision(

    imageBlob,

    camera

){

    const formData = new FormData();

    formData.append(

        "image",

        imageBlob,

        "frame.jpg"

    );

    formData.append(

        "camera",

        camera

    );
        
        formData.append(

        "mode",

        "vision"

    );

    const response = await api.post(

        "/vision/analyze",

        formData,

        {

            headers:{

                "Content-Type":"multipart/form-data"

            }

        }

    );

    return response.data;

}