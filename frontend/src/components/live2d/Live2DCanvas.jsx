import { useEffect, useRef } from "react";
import { LAppDelegate } from "../../live2d/app/lappdelegate";


export default function Live2DCanvas(){

    const canvasRef = useRef(null);


    useEffect(()=>{


        console.log("CANVAS START");


        const delegate =
            LAppDelegate.getInstance();

    
        delegate.initialize();

    
        delegate.run();

         const canvas = canvasRef.current;
            if (!canvas) return;

            // 🔥 FIX MOBILE INPUT
            const getPos = (e) => {
                const rect = canvas.getBoundingClientRect();

                return {
                    x: e.clientX - rect.left,
                    y: e.clientY - rect.top
                };
            };

        // 🔥 IMPORTANT: attach input ke canvas
        canvas.addEventListener("pointerdown", (e) => {
            delegate.onPointerDown?.(e.clientX, e.clientY);
        });

        canvas.addEventListener("pointermove", (e) => {
            delegate.onPointerMove?.(e.clientX, e.clientY);
        });

        canvas.addEventListener("pointerup", (e) => {
            delegate.onPointerUp?.(e.clientX, e.clientY);
        });

        canvas.addEventListener("pointerleave", (e) => {
            delegate.onPointerUp?.(e.clientX, e.clientY);
        });


        const subdelegate =
        delegate.getSubdelegate();


        const manager =
        subdelegate.getLive2DManager();


        const model =
        manager.getModel();


        window.live2dModel = model;


        console.log(
            "MODEL GLOBAL =",
            window.live2dModel
        );


        setTimeout(()=>{


            const manager =
                delegate.getLive2DManager();



            const model =
                manager.getModel();



            window.live2dModel =
                model;



            console.log(
                "LIVE2D CONNECTED",
                model
            );


        },1500);





    },[]);




    return (

        <div className="live2d-container">

            <img
                src="/bg/room.jpg"
                alt="background"
                className="live2d-background"
            />

            <canvas

                id="live2d"

                ref={canvasRef}

                className="live2d-canvas"

            />

        </div>

    

    );
}