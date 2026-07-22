import { useState } from "react";

import BottomBar from "./BottomBar";

import {
  MessageCircle,
  Heart,
  Volume2,
  Sparkles,
  Languages
} from "lucide-react";

import { translateText } from "../api";


export default function ChatPanel({
  messages,
  input,
  setInput,
  handleSend,
  isTyping,
  researchMode,
  setResearchMode,
  visionEnabled,
  setVisionEnabled
}) {


  const [translations,setTranslations] = useState({});



  return (

    <div className="chat-panel">


      <div className="chat-header">
        Chat
      </div>



      <div className="chat-messages">


      {messages.length === 0 ? (


        <div className="welcome-screen">


          <h2>
            Welcome, I'm Aoi ✨
          </h2>


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



        messages.map((msg,index)=>(


          <div

            key={index}

            className={`message ${msg.role}`}

          >



            <div className="message-role">

              {
                msg.role === "user"
                ?
                "You:"
                :
                "Aoi Chisei:"
              }

            </div>



            <div className="message-content">


              {msg.content}



              {
                msg.role === "assistant" && (

                  <button

                    className="translate-btn"

                    onClick={async()=>{


                      try{


                        const result =
                        await translateText(
                          msg.content
                        );



                        setTranslations(prev=>({

                          ...prev,

                          [index]:
                          result.translation

                        }));


                      }
                      catch(err){

                        console.log(
                          "Translate error:",
                          err
                        );

                      }


                    }}

                  >

                   <Languages size={16}/>

                   <span>Translate</span>

                  </button>


                )
              }




              {
                translations[index] && (

                  <div className="translation">


                    {translations[index]}


                  </div>

                )
              }



            </div>


          </div>



        ))



      )}




      {
        isTyping && (

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

        )
      }



      </div>



      <BottomBar

        input={input}

        setInput={setInput}

        handleSend={handleSend}

        researchMode={researchMode}

        setResearchMode={setResearchMode}

        visionEnabled={visionEnabled}
        setVisionEnabled={setVisionEnabled}

      />



    </div>

  );

}
