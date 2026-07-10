import { useEffect } from "react";
import "./SplashScreen.css";

export default function SplashScreen({enter}){


     useEffect(()=>{

        if(enter){

            const audio = new Audio(
                "/audio/portal.mp3"
            );

            audio.volume = 0.8;

            audio.play()
            .catch(err=>{
                console.log("Audio blocked:",err);
            });

        }


    },[enter]);

    return(

        <div className="splash">


            <div className="splash-glow"></div>


            <div className="splash-content">


                <img
                    src="/assets/torii-gate.png"
                    className="torii-logo"
                    alt="Isekai Gate"
                />


                <h1 className="app-title">
                    ISEKAI GATE
                </h1>


                <p className="subtitle">
                    AI Companion
                </p>



                <div className="loading-text">
                    Loading your world...
                </div>


                <div className="progress">

                    <div className="progress-bar"></div>

                </div>


            </div>


            {enter && (

            <div className="portal-transition">

                <img
                    src="/assets/torii-gate.png"
                    className="portal-image"
                    alt="Portal"
                />

                <div className="portal-flash"></div>

            </div>

        )}                                                                     


        </div>

    )
}