import BottomBar from "./BottomBar";
import {
  Mic,
  Eye,
  Brain,
  MapPin
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

      <h2>Hi, I'm Aoi</h2>

      <p>I can help you with:</p>

      <div className="welcome-features">

        <div className="feature-card">
            <Mic size={20}/>
             <span>Voice Chat</span>
        </div>

        <div className="feature-card">
           <Eye size={20}/>
           <span>Vision</span>
        </div>

        <div className="feature-card">
          <Brain size={20}/>
          <span>Memory</span>
        </div>

        <div className="feature-card">
          <MapPin size={20}/>
          <span>Navigation</span>
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
