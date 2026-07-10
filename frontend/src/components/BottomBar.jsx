import {
  Camera,
  Mic,
  Send
} from "lucide-react";
import {useState} from "react";


export default function BottomBar({
  input,
  setInput,
  handleSend
}) {

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
        placeholder="Message Aoi..."
        />
        <button
          onClick={()=>{
            setPopup("Voice Chat Coming Soon");
          }}
        >
          <Mic size={20} />
       </button>
        
      <button 
            className="send-btn"
            onClick={handleSend}
      >
      
        <Send size={20} />
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