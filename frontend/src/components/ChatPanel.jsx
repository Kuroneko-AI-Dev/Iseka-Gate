import BottomBar from "./BottomBar";
import {
  Mic,
  Eye,
  Brain,
  MapPin,
  MessageCircle, 
  Heart,
  Volume2,
  Sparkles
} from "lucide-react";
export default function ChatPanel({
  messages,
  input,
  setInput,
  handleSend,
  isTyping
}) {

  return (
    <div className="chat-panel">

      <div className="chat-header">
        Chat
      </div>

      <div className="chat-messages">

  {messages.length === 0 ? (

   <div className="welcome-screen">

  <h2>Welcome, I'm Aoi ✨</h2>

  <p>
    Your AI companion is ready.
  </p>


  <div className="welcome-features">

    <div className="feature-card">
      <MessageCircle size={20}/>
      <span>
        Talk with Aoi
      </span>
    </div>


    <div className="feature-card">
      <Heart size={20}/>
      <span>
        Remember your story
      </span>
    </div>


    <div className="feature-card">
      <Volume2 size={20}/>
      <span>
        Natural Voice
      </span>
    </div>


    <div className="feature-card">
      <Sparkles size={20}/>
      <span>
        Anime Personality
      </span>
    </div>

  </div>

</div>

  ) : (

    messages.map((msg, index) => (
      <div
        key={index}
        className={`message ${msg.role}`}
      >
        {msg.content}
      </div>
    ))

  )}

  {isTyping && (
  <div className="typing-indicator">

    <div className="typing-text">
      Aoi is typing...
    </div>

    <div className="typing-dots">
      <span></span>
      <span></span>
      <span></span>
    </div>

  </div>
)}

</div>

      <BottomBar
        input={input}
        setInput={setInput}
        handleSend={handleSend}
      />

    </div>
  );
}
