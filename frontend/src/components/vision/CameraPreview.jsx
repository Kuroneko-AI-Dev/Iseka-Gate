import {
    forwardRef,
    useEffect,
    useRef,
    useImperativeHandle,
    useState
} from "react";
import "./CameraPreview.css";
import { Camera, Repeat, RotateCw } from "lucide-react";
 const CameraPreview = forwardRef(function CameraPreview(

    { enabled },

    ref

) {

    const videoRef = useRef(null);
    
    const [stream, setStream] = useState(null);
    const [facingMode, setFacingMode] = useState("environment");




    useImperativeHandle(ref, () => ({

    async captureFrame() {

        if (!videoRef.current) {
            return null;
        }

        const video = videoRef.current;

        const canvas = document.createElement("canvas");

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");

        ctx.drawImage(
            video,
            0,
            0,
            canvas.width,
            canvas.height
        );

        return await new Promise((resolve) => {

            canvas.toBlob(

                (blob) => {

                    resolve(blob);

                },

                "image/jpeg",

                0.9

            );

        });

    }

}));
    async function startCamera(mode = facingMode){

        try{

            if(!navigator.mediaDevices){

            console.error(
                "mediaDevices tidak tersedia"
            );

            return;

        }

            const media =
            await navigator.mediaDevices.getUserMedia({

                video:{
                    facingMode:mode
                },

                audio:false

            });

            if(videoRef.current){

                videoRef.current.srcObject = media;

                console.log("VIDEO STREAM:", media);

                await videoRef.current.play();

            }

            setStream(media);

        }catch(err){

            console.error("Camera Error:",err);

        }

    }

    function stopCamera(){

        if(stream){

            stream
            .getTracks()
            .forEach(track=>track.stop());

            setStream(null);

        }

    }

    useEffect(()=>{

        if(enabled){

            startCamera();

        }else{

            stopCamera();

        }

        return ()=>{

            stopCamera();

        };

    },[enabled]);

    async function switchCamera(){

        const next =

            facingMode==="environment"
            ? "user"
            : "environment";

        stopCamera();

        setFacingMode(next);

        await startCamera(next);

    }

    if(!enabled){

        return null;

    }

    return(

        <div className="camera-preview">

            <video
                ref={videoRef}
                autoPlay
                muted
                playsInline
                className="camera-vidio"
                
    
            />

            <button
                className="camera-switch"
                onClick={switchCamera}
            >
                <Repeat size={18}/>
            </button>

        </div>

    );

});

export default CameraPreview;

