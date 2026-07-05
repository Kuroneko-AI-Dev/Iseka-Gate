import {
  Camera,
  Mic,
  Send
} from "lucide-react";


export default function BottomBar({
  input,
  setInput,
  handleSend
}) {
  return (
    <div className="bottom-bar">

      <button>
        <Camera size={20} />
      </button>

      <button>
        <Mic size={20} />
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
        placeholder="Ketik pesan..."
        />
      <button onClick={handleSend}>
        <Send size={20} />
      </button>

    </div>
  );
}