import { useEffect } from "react";
import "./SplashScreen.css";

export default function SplashScreen({ enter }) {

    useEffect(() => {

        const audio = new Audio("/audio/dodoco.mp3");

        audio.loop = true;
        audio.volume = 0.8;

        audio.play()
        .catch(err=>{
            console.log("Audio blocked:", err);
        });

          const timer = setTimeout(()=>{

            enter();

        },17000);


        return () => {
            audio.pause();
            audio.currentTime = 0;
            clearTimeout(timer);
        };

    }, []);


    return (
        <div className="splash">

                <img
                    src="/assets/aoi-mobile.png"
                    className="torii-logo"
                    alt="Isekai Gate"
                />

          

            <div className="splash-content">


                <div className="progress">
                    <div className="progress-bar"></div>
                </div>

            </div>

        </div>
    );
}