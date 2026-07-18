import {
  Camera,
  Mic,
  Send,
  Search
} from "lucide-react";
import {useState} from "react";
import {
  speechToText
} from "../api";

export default function BottomBar({
  input,
  setInput,
  handleSend,
  researchMode,
  setResearchMode
}) {
 
  const [recording,setRecording] = useState(false);
  const [recorder,setRecorder] = useState(null);
  const [popup, setPopup] = useState("");
  return (
    <div className="bottom-bar">
      <div className="chat-input-box">
       
      <button
          onClick={()=>{
            setPopup("Vision Camera Coming Soon");
          }}
        >
          <Camera size={20} />
        </button>

        <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
            }
        }}
        placeholder={researchMode ? "Ask Aoi to research the web..." : "Message Aoi..."}
        />

         {
          recording && (
            <div className="recording-info">
               Listening... Tekan Mic lagi untuk berhenti
            </div>
          )
          }
      <button
  className={recording ? "mic-recording" : ""}
  onClick={async()=>{


  if(!recording){

     

      const stream =
      await navigator.mediaDevices.getUserMedia({
          audio:true
      });

      const mediaRecorder = new MediaRecorder(stream);

      let chunks=[];


      mediaRecorder.ondataavailable=e=>{
          chunks.push(e.data);
      };


      mediaRecorder.onstop=async()=>{

        setPopup("");

        stream.getTracks().forEach((track)=>track.stop());


        const blob = new Blob(chunks,{
          type:"audio/webm"
        });


        const result = await speechToText(blob);


        if(result?.text){
          handleSend(String(result.text));
        }

      };


      mediaRecorder.start();

      setRecorder(mediaRecorder);
      setRecording(true);


  }else{

    

      if(recorder && recorder.state !== "inactive"){
          recorder.stop();
      }

      setRecording(false);

  }


  }}
>
<Mic size={20}/>
</button>
        
     <button
        className="send-btn"
        onClick={()=>{
        handleSend();
        }}
        >
        <Send size={20}/>
    </button>
      </div>

      {
      popup && (

      <div
        className="coming-popup"
        onClick={()=>{
          setPopup("");
        }}
      >

        <div
          className="coming-box"
          onClick={(e)=>e.stopPropagation()}
        >

          <h3>
            🚀 Coming Soon
          </h3>

          <p>
            {popup}
          </p>

          <button 
            onClick={()=>{
              setPopup("");
            }}
          >
            OK
          </button>

          

          

        </div>
        
        

      </div>
      

    

      )
      }
      

    </div>
  );
}
