import { useState } from "react";
import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "../firebase";
import api from "../api/axios";
import { googleLogin as googleLoginAPI } from "../api/auth";


export default function LoginPage({ onLogin, onRegister }) {


  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  const [loading,setLoading] = useState(false);
  const [error,setError] = useState("");



  // LOGIN EMAIL PASSWORD
  async function handleLogin(){

    setLoading(true);
    setError("");

    try{

      const res = await api.post(
        "/auth/login",
        {
          email,
          password
        }
      );


      localStorage.setItem(
        "token",
        res.data.access_token
      );


      localStorage.setItem(
        "user",
        JSON.stringify({
          username: res.data.username,
          plan: res.data.plan,
          avatar: res.data.avatar
        })
      );


      if(onLogin){
        onLogin();
      }


    }
    catch (err) {

    console.error("GOOGLE ERROR:", err);

    if (err.response) {

        console.log("STATUS:", err.response.status);
        console.log("DATA:", err.response.data);

        alert(JSON.stringify(err.response.data));

    } else {

        alert(err.message);

    }

}

    setLoading(false);

  }




  // LOGIN GOOGLE
  async function handleGoogleLogin(){

    try{


      const result = await signInWithPopup(
        auth,
        googleProvider
      );


      const idToken =
        await result.user.getIdToken();



      const data =
        await googleLoginAPI(idToken);
        console.log(data)



      localStorage.setItem(
        "token",
        data.access_token
      );


      localStorage.setItem(
        "user",
        JSON.stringify({
          username:data.username,
          plan:data.plan,
          avatar:data.avatar
        })
      );



      if(onLogin){
        onLogin();
      }



    }catch(err){

      console.log(err);

      setError(
        "Google Login gagal"
      );

    }

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

<source src="/portal.mp4" type="video/mp4" />

</video>



<div className="login-overlay"></div>



<div className="login-card">



<div className="login-logo">

<img src="/login.png" alt="Raphael" />

</div>



<p className="login-subtitle">

Please enter your email and password to login

</p>





<input

className="login-input"

type="email"

placeholder="Email"

value={email}

onChange={
e=>setEmail(e.target.value)
}

/>





<input

className="login-input"

type="password"

placeholder="Password"

value={password}

onChange={
e=>setPassword(e.target.value)
}

/>





{error && (

<p style={{color:"red"}}>

{error}

</p>

)}






<button

className="login-button"

onClick={handleLogin}

disabled={loading}

>

{loading ? "Checking..." : "Login"}

</button>





<div className="login-divider">

<span>OR</span>

</div>





<button

className="google-button"

onClick={handleGoogleLogin}

>

Continue with Google

</button>





<p

className="register-link"

onClick={onRegister}

>

Belum punya akun? Register

</p>





<div className="login-status">


<span className="login-status-dot"></span>


Raphael Online


</div>



</div>



</div>

);

}