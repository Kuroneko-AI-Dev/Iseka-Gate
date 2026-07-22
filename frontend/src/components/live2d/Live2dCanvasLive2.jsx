import { useEffect, useRef } from "react";
import { LAppDelegate } from "../../live2d/app/lappdelegate";


export default function Live2DCanvas(){

    const canvasRef = useRef(null);
    const started = useRef(false);


    useEffect(()=>{


        // cegah React StrictMode start 2x
        if(started.current){
            console.log("LIVE2D ALREADY STARTED");
            return;
        }

        started.current = true;


        console.log("CANVAS START");


        const delegate =
            LAppDelegate.getInstance();



        // initialize hanya sekali
        if(!delegate._initialized){

            delegate.initialize();

            delegate._initialized = true;

            console.log("LIVE2D INITIALIZED");

        }


       


        const canvas = canvasRef.current;


        if(!canvas){

            console.log("CANVAS NOT FOUND");

            return;

        }



        // ambil manager yang benar
        const subdelegate =
            delegate.getSubdelegate();



        if(!subdelegate){

            console.log("SUBDELEGATE NOT FOUND");

            return;

        }



        const manager =
            subdelegate.getLive2DManager();



        if(!manager){

            console.log("MANAGER NOT FOUND");

            return;

        }



        const model =
            manager.getModel();



        window.live2dModel = model;



        console.log(
            "MODEL GLOBAL =",
            model
        );



        // tunggu model selesai load
        const timer = setTimeout(()=>{


            const subdelegate =
                delegate.getSubdelegate();



            const manager =
                subdelegate?.getLive2DManager();



            const model =
                manager?.getModel();



            if(model){

                window.live2dModel = model;


                console.log(
                    "LIVE2D CONNECTED",
                    model
                );

            }


        },1500);



        return ()=>{


            clearTimeout(timer);


            console.log(
                "LIVE2D COMPONENT CLEANUP"
            );


        };


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

                

                className="live2d-canvas"

            />


        </div>

    );

}