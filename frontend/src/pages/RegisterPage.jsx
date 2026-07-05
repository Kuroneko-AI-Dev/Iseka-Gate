import {useState} from "react";
import api from "../api/axios";


export default function RegisterPage({onLoginPage}){


const [username,setUsername]=useState("");
const [email,setEmail]=useState("");
const [password,setPassword]=useState("");
const [error,setError]=useState("");
const [loading,setLoading]=useState(false);



async function register(){


try{

setLoading(true);
setError("");


await api.post(
"/auth/register",
{
 username,
 email,
 password,
 avatar:"/avatars/default.png"
}
);


onLoginPage();


}catch(err){

console.log(err);

setError(
"Email mungkin sudah digunakan"
);

}


setLoading(false);

}



return (

<div className="login-page">


<video
className="login-video"
autoPlay
muted
loop
playsInline
>

<source 
src="/intro.mp4"
type="video/mp4"
/>

</video>



<div className="login-overlay"></div>



<div className="login-card">


<div className="login-logo">

<img 
src="/login.png"
alt="Raphael"
/>

</div>



<p className="login-subtitle">
Create Raphael Account
</p>



<input
className="login-input"
placeholder="Username"
onChange={
e=>setUsername(e.target.value)
}
/>



<input
className="login-input"
type="email"
placeholder="Email"
onChange={
e=>setEmail(e.target.value)
}
/>



<input
className="login-input"
type="password"
placeholder="Password"
onChange={
e=>setPassword(e.target.value)
}
/>



{
error &&
<p style={{color:"red"}}>
{error}
</p>
}



<button
className="login-button"
onClick={register}
>

{
loading
?"Creating..."
:"Register"
}

</button>



<p
  className="account-switch"
  onClick={onLoginPage}
>
  Sudah punya akun? Login
</p>


</div>


</div>

)

}