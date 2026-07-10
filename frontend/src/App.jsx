import { useState, useEffect } from "react";
import SplashScreen from "./components/SplashScreen";
import { getProfile } from "./api/user";

import AdminDashboard from "./pages/AdminDashboard";
import {
  sendMessage,
  getConversations,
  getMessages,
  renameConversation,
  deleteConversation,
  activatePremium,
  createPayment
} from "./api";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import SettingsPage from "./pages/SettingsPage";
import AvatarStage from "./components/AvatarStage";
import ChatPanel from "./components/ChatPanel";
import { LogOut, Menu } from "lucide-react";
import {
  MessageCircle,
  Eye,
  Brain,
  Mic,
  Settings,
  Crown,House
} from "lucide-react";
import { API_URL } from "./config";
import "./App.css";
import PremiumModal from "./components/PremiumModal";


export default function App() {


  const [isTyping, setIsTyping] = useState(false);
  const [messages, setMessages] = useState([]);
  const [activeChat,setActiveChat] = useState(null);
  const [input, setInput] = useState("");
  const [conversationId,setConversationId] = useState(null);
  const [conversations,setConversations] = useState([]);
  const [showHistory,setShowHistory] = useState(false);
  const [menuChatId, setMenuChatId] = useState(null);
  const [renameChat,setRenameChat] = useState(null);
  const [renameText,setRenameText] = useState("");
  const [deleteChat, setDeleteChat] = useState(null);
  const [currentPage, setCurrentPage] = useState("chat");
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  const [showPremium,setShowPremium]=useState(false);
  const [page, setPage] = useState("login");
  const [loading,setLoading]=useState(false);
  const [enter,setEnter]=useState(false);


const isStandalone =
window.matchMedia("(display-mode: standalone)").matches ||
window.navigator.standalone === true;
/*useeffect time*/
useEffect(()=>{

    if(isStandalone){

        setLoading(true);


        const timer=setTimeout(()=>{

            setEnter(true);


            setTimeout(()=>{

                setLoading(false);

            },800);


        },2500);


        return ()=>clearTimeout(timer);

    }

},[]);


  const [user, setUser] = useState(()=>{
    const saved = localStorage.getItem("user");

    return saved
      ? JSON.parse(saved)
      : null;
  });

   function resetChatState() {

    setMessages([]);
    setConversationId(null);
    setConversations([]);
    setActiveChat(null);
    setShowHistory(false);
    setMenuChatId(null);
    setRenameChat(null);
    setRenameText("");
    setDeleteChat(null);
    setInput("");
    setCurrentPage("chat");

  }


  // ambil data user dari backend
  useEffect(()=>{

  if(isLoggedIn){

    getProfile()
    .then(data=>{

      setUser(data);

      localStorage.setItem(
        "user",
        JSON.stringify(data)
      );

    })
    .catch(console.log);



    getConversations()
    .then(data=>{

      setConversations(data);

    })
    .catch(console.log);

  }

},[isLoggedIn]);


  async function handleSend(){


    if(!input.trim()) return;


    const userText = input;


    setMessages(prev=>[
      ...prev,
      {
        role:"user",
        content:userText
      }
    ]);


    setInput("");



    try{


      setIsTyping(true);


      const voice =

        localStorage.getItem("voice") ||

        "Leda";

        const result = await sendMessage(

            userText,

            conversationId,

            voice

        );


      setConversationId(
        result.conversation_id
      );
      const chats = await getConversations();

      setConversations(chats);

      setIsTyping(false);



      setMessages(prev=>[
        ...prev,
        {
          role:"assistant",
          content:result.text
        }
      ]);



      const audioUrl = `${API_URL}/${result.audio}`;

      const audio = new Audio(audioUrl);


      audio.play();


      // SEND AUDIO TO LIVE2D LIPSYNC
      if(window.live2dModel){

          window.live2dModel.startLipSync(
              audioUrl
          );

      }

    



    }catch{


      setMessages(prev=>[
        ...prev,
        {
          role:"assistant",
          content:"Backend tidak terhubung."
        }
      ]);

    }

  }




  if(loading){

      return <SplashScreen enter={enter}/>;

  }

  // belum login
  if(!isLoggedIn){


    return page==="login" ?


    <LoginPage

      onLogin={()=>{

        setIsLoggedIn(true);


        const saved =
        localStorage.getItem("user");


        if(saved){

          setUser(
            JSON.parse(saved)
          );

        }

      }}


      onRegister={()=>{

        setPage("register");

      }}

    />


    :


    <RegisterPage

      onLoginPage={()=>{

        setPage("login");

      }}

    />

  }



  if (user?.is_admin && currentPage === "admin") {
    return <AdminDashboard />;
}


  return (

    <div className={`app ${isStandalone ? "standalone" : ""}`}>



      <aside className="sidebar">



        <div className="logo">

          <img
            src="/logo.png"
            alt="Logo"
          />

        </div>

      <div className="menu">


        <button
          onClick={() => {

            setConversationId(null);
            setMessages([]);
            setActiveChat(null);
            setShowHistory(false);

          }}
        >
          <MessageCircle />
        </button>


        <button
          className="brain-menu"
          onClick={()=>{
            setShowHistory(!showHistory)
          }}
        >
          <Brain />
        </button>


        <button
          onClick={()=>{
            setShowPremium(true);
          }}
        >
          <Crown />
        </button>


        <button
          onClick={() => {

            if(currentPage==="settings"){

                setCurrentPage("chat");

            }else{

                setCurrentPage("settings");

                setShowHistory(false);

            }

          }}
        >
          <Settings />
        </button>


        </div>
              
        <div className="account-section">


          <div className="user-card">



          <img
              key={user?.id}
              src={user?.avatar || "/avatar.png"}
              alt="User"
              className="user-avatar"
              referrerPolicy="no-referrer"
            />



            <div className="user-info">


              <div className="user-name">

                {
                  user?.username ||
                  "Guest User"
                }

              </div>
 


              <div className="user-status">

                {
                  user?.plan ||
                  "FREE"
                }
                {" "}PLAN

                 
              </div>

               <button
                      className="premium-btn"
                     onClick={async()=>{

                        setShowPremium(true);
                      
                        const result = await createPayment("monthly");

                        console.log(result);

                        alert(result.message);

                    }}
                                      >
                      Upgrade
                  </button>




            </div>





            <button

              className="signin-btn"

              onClick={() => {

                localStorage.removeItem("token");
                localStorage.removeItem("user");

                setUser(null);
                setIsLoggedIn(false);

                // Reset semua state chat
                setMessages([]);
                setConversationId(null);
                setConversations([]);
                setActiveChat(null);
                setShowHistory(false);
                setMenuChatId(null);
                setRenameChat(null);
                setDeleteChat(null);
                setInput("");
                setCurrentPage("chat");

            }}
            >
              <LogOut size={16} />

               <span>Logout</span>

              

            </button>



          </div>


        </div>



      </aside>








      <main className="main-content">



        <div className="topbar">


          <div className="header-info">


            <div className="header-title">

               AI Companion

            </div>



            <div className="header-status">

              <span className="status-dot"></span>

              Online • New Model • Voice Ready

            </div>



          </div>



        </div>

       

       <div className="content">

          <div className="avatar-column">

            {showHistory && (

              <div className="history-panel">

                <button
                  className="new-chat-btn"
                  onClick={()=>{
                    setConversationId(null);
                    setMessages([]);
                    setShowHistory(false);
                  }}
                >
                  + New Chat
                </button>

                <div className="history-list">

                 {conversations.map(chat=>(

                  <div
                    className="history-item-wrap"
                    key={chat.id}
                  >


                  <button

                  className="history-row"

                  onClick={async()=>{

                  const data =
                  await getMessages(chat.id);


                  setMessages(
                  data.map(m=>({
                  role:m.role,
                  content:m.content
                  }))
                  );


                  setConversationId(chat.id);

                  setShowHistory(false);

                  }}

                  >

                  {chat.title}

                  </button>



                  <button

                  className="history-more"

                 onClick={(e)=>{

                      e.stopPropagation();

                      if(menuChatId===chat.id){

                          setMenuChatId(null);

                      }else{

                          setMenuChatId(chat.id);

                      }

                  }}

                  >

                  ⋮

                  </button>
                {menuChatId===chat.id && (

                  <div className="history-menu">

                  <button

                 onClick={() => {

                      setRenameChat(chat);

                      setRenameText(chat.title);

                      setMenuChatId(null);

                  }}

                  >

                  ✏ Rename

                  </button>

                  <button

                 onClick={() => {

                      setDeleteChat(chat);

                      setMenuChatId(null);

                  }}

                  >

                  🗑 Delete

                  </button>

                  </div>

                  )}


                  </div>

                  ))}
                </div>

              </div>

            )}

            <AvatarStage />

          </div>

          <div className="chat-column">

            {currentPage !== "settings" && (
              <button
                  className="mobile-menu-btn"
                  onClick={() => setShowMobileMenu(!showMobileMenu)}
              >
                  <Menu />
              </button>
          )}

  <ChatPanel
    messages={messages}
    input={input}
    setInput={setInput}
    handleSend={handleSend}
    isTyping={isTyping}
  />

  {currentPage === "settings" && (
    <div className="settings-overlay">

      <button
        className="settings-back"
        onClick={() => setCurrentPage("chat")}
      >
        <House size={18} />
        Home
      </button>

      <SettingsPage
          user={user}
          onOpenAdmin={() => setCurrentPage("admin")}
      />

    </div>
  )}

</div>

    </div>

         {showMobileMenu && (
  <div className="mobile-menu">

    <button onClick={()=>{
      setCurrentPage("chat");
      setShowHistory(false);
      setShowMobileMenu(false);
    }}>
      <MessageCircle size={18}/>
      <span>Chat</span>
    </button>

    <button onClick={()=>{
      setShowHistory(!showHistory);
      setShowMobileMenu(false);
    }}>
      <Brain size={18}/>
      <span>History</span>
    </button>

    <button
      onClick={()=>{
        setShowPremium(true);
        setShowMobileMenu(false);
      }}
    >
      <Crown size={18}/>
      <span>Premium</span>
    </button>

    <button onClick={()=>{
      setCurrentPage("settings");
      setShowHistory(false);
      setShowMobileMenu(false);
    }}>
      <Settings size={18}/>
      <span>Settings</span>
    </button>

  </div>
)}



      </main>
            
    {
      renameChat && (

      <div className="rename-overlay">


      <div className="rename-box">


      <h3>
      Rename Chat
      </h3>


      <input

      value={renameText}

      onChange={(e)=>
      setRenameText(e.target.value)
      }

      />


      <div className="rename-actions">


      <button

      onClick={()=>{
      setRenameChat(null);
      }}

      >
      Cancel
      </button>


      <button

      onClick={async()=>{


      await renameConversation(
      renameChat.id,
      renameText
      );


      const data =
      await getConversations();


      setConversations(data);


      setRenameChat(null);


      }}

      >
      Save
      </button>


      </div>


      </div>

      </div>

      )
      }

{deleteChat && (

<div className="delete-overlay">

  <div className="delete-box">

    <h3>Delete Conversation</h3>

    <p>
      This conversation will be permanently deleted.
    </p>

    <div className="delete-actions">

      <button
        onClick={()=>{
          setDeleteChat(null);
        }}
      >
        Cancel
      </button>

      <button

        className="delete-btn"

        onClick={async()=>{

          await deleteConversation(deleteChat.id);

          const data =
          await getConversations();

          setConversations(data);

          if(conversationId===deleteChat.id){

            setConversationId(null);

            setMessages([]);

          }

          setDeleteChat(null);

        }}

      >
        Delete
      </button>

    </div>

  </div>

</div>

)}

  <PremiumModal
    open={showPremium}
    onClose={() => setShowPremium(false)}
    user={user}
    onUpgrade={async () => {

        await activatePremium();

        const profile = await getProfile();

        setUser(profile);

        localStorage.setItem(
            "user",
            JSON.stringify(profile)
        );

        setShowPremium(false);

    }}
/>



    </div>

  );

}