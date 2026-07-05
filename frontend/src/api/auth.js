import axios from "axios"
import { API_URL } from "../config";


export async function googleLogin(idToken){

    const response = await axios.post(
        `${API_URL}/auth/google`,
        {
            id_token: idToken
        }
    )


    return response.data
}