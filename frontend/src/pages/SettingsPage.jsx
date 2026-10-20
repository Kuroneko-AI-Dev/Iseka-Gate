import { useState } from "react";
import {
    Settings,
    Palette,
    Mic,
    Brain,
    Cpu,
    User,
    Info,
    Shield,
    ChevronDown,
    Check,
    Sparkles
} from "lucide-react";

import "./SettingsPage.css";
import ManageMemory from "./settings/ManageMemory";


export default function SettingsPage({
    user,
    onOpenAdmin,
    avatarScale,
    setAvatarScale
}){

    const [tab,setTab]=useState("general");
  
    const [avatarY, setAvatarY] = useState(() => {
    const saved = localStorage.getItem("avatarY");
    return saved !== null ? Number(saved) : -14.4;
});
    const [voice,setVoice]=useState(

    localStorage.getItem("voice") ||

    "Leda"

);  const voices = [
    "Despina",
    "Aoede",
    "Kore",
    "Puck",
    "Leda",
    "Charon"
];

    const [showAdminDenied, setShowAdminDenied] = useState(false);
    const [openVoice, setOpenVoice] = useState(false);
    const [showMemory,setShowMemory]=useState(false);
    const [style,setStyle] = useState(
    localStorage.getItem("style") || ""
);

  const changeScale = (amount) => {
    const newScale = Math.max(
        0.5,
        Math.min(
            2.5,
            Number((avatarScale + amount).toFixed(2))
        )
    );

    setAvatarScale(newScale);
};


const changeY = (amount) => {
    const newY = Number(
        (avatarY + amount).toFixed(1)
    );

    if (window.moveLive2DY) {
        window.moveLive2DY(
            newY - avatarY
        );
    }

    setAvatarY(newY);

    localStorage.setItem(
        "avatarY",
        newY
    );
};


const setScaleDefault = () => {
    const defaultScale = 1.0;

    // Trigger scale yang sama seperti slider
    setAvatarScale(defaultScale);

    // Simpan
    localStorage.setItem(
        "avatarScale",
        defaultScale
    );
};


const setYDefault = () => {
    const defaultY = -10.2;

    // Trigger Y yang sama seperti tombol/slider Y
    if (window.moveLive2DY) {
        window.moveLive2DY(
            defaultY - avatarY
        );
    }

    // Update React
    setAvatarY(defaultY);

    // Simpan
    localStorage.setItem(
        "avatarY",
        defaultY
    );
};


const setCharacterDefault = () => {
    // Jalankan DEFAULT SCALE
    setScaleDefault();

    // Jalankan DEFAULT Y
    setYDefault();
};
    return(

        <div className="settings-page">
            

            <div className="settings-sidebar">
               <button
                    className={`settings-nav-item ${
                        tab === "character" ? "active" : ""
                    }`}
                    onClick={() => setTab("character")}
                >
                    <Sparkles size={18} />
                    <span>Character</span>
                </button>
                <button
                    className={tab==="general"?"active":""}
                    onClick={()=>setTab("general")}
                >
                    <Settings size={18}/>
                    <span>General</span>
                </button>

                <button
                    className={tab==="appearance"?"active":""}
                    onClick={()=>setTab("appearance")}
                >
                    <Palette size={18}/>
                    <span>Appearance</span>
                </button>

                <button
                    className={tab==="voice"?"active":""}
                    onClick={()=>setTab("voice")}
                >
                    <Mic size={18}/>
                    <span>Voice</span>
                </button>

                <button
                    className={tab==="memory"?"active":""}
                    onClick={()=>setTab("memory")}
                >
                    <Brain size={18}/>
                    <span>Memory</span>
                </button>

                <button
                    className={tab==="model"?"active":""}
                    onClick={()=>setTab("model")}
                >
                    <Cpu size={18}/>
                    <span>AI Model</span>
                </button>

                <button
                    className={tab==="account"?"active":""}
                    onClick={()=>setTab("account")}
                >
                    <User size={18}/>
                    <span>Account</span>
                </button>

                <button
                    className={tab==="about"?"active":""}
                    onClick={()=>setTab("about")}
                >
                    <Info size={18}/>
                    <span>About</span>
                </button>

       
 

        <div
            className="admin-dashboard-btn"
            onClick={() => {

                if(user?.is_admin){

                onOpenAdmin();

                }else{

               setShowAdminDenied(true);

                }

            }}
            >
                <Shield size={18}></Shield>
            <span> Admin Dashboard</span>

            </div>   
            </div>

            <div className="settings-content">
                
            {tab === "character" && (
    <div className="character-settings">
        <h2>Character</h2>

    

       <div className="setting-card">

    <h4>Character Size</h4>

    <p>
        Adjust the size of your AI companion.
    </p>

    <div className="avatar-scale-control">

        <div className="avatar-scale-label">

            <span>Scale</span>

            <span>
                {Math.round(avatarScale * 100)}%
            </span>

        </div>

        <div className="avatar-number-controls">

            <button
                type="button"
                onClick={() => changeScale(-0.05)}
            >
                −
            </button>

            <input
                type="range"
                min="0.5"
                max="2.5"
                step="0.05"
                value={avatarScale}
                onChange={(e) =>
                    setAvatarScale(
                        Number(e.target.value)
                    )
                }
            />

            <button
                type="button"
                onClick={() => changeScale(0.05)}
            >
                +
            </button>

        </div>

    </div>

   <button
    type="button"
    className="character-set-btn"
    onClick={setCharacterDefault}
>
    Set Character Default
</button>

</div>
        <div className="setting-card">

    <h4>Character Position</h4>

    <p>
        Move your AI companion up or down.
    </p>

    <div className="avatar-scale-control">

        <div className="avatar-scale-label">

            <span>Position Y</span>

            <span>
                {avatarY}
            </span>

        </div>

        <button
        type="button"
        onClick={() => changeY(-0.1)}
    >
        −
    </button>

        <input
            type="range"
            min="-15"
            max="2"
            step="0.1"
            value={avatarY}
            onChange={(e) => {
                const value = Number(e.target.value);

                setAvatarY(value);

                    localStorage.setItem(
                        "avatarY",
                        value
                    );

                    if (window.moveLive2DY) {
                        window.moveLive2DY(
                            value - avatarY
                        );
                    }
            }}
        />

         <button
        type="button"
        onClick={() => changeY(0.1)}
    >
        +
    </button>

    </div>
 
    

</div>

</div>


   
    
)}

                {tab==="general" && (
                    <>
                        <h2>General</h2>

                        <div className="setting-card">
                           <div className="setting-card">

                            <h4>Response Style</h4>

                            <textarea

                                className="style-input"

                                value={style}

                                placeholder="Contoh: jawab dengan tenang, dingin, seperti anime"

                                onChange={(e)=>{

                                    setStyle(e.target.value);

                                    localStorage.setItem(
                                        "style",
                                        e.target.value
                                    );

                                }}

                            />

                        </div>
                        </div>

                        <div className="setting-card">
                            <h4>Auto Save</h4>
                            <label className="switch">
                                <input type="checkbox" defaultChecked/>
                                <span></span>
                            </label>
                        </div>
                    </>
                )}

                {tab==="appearance" && (
                    <>
                        <h2>Appearance</h2>

                        <div className="setting-card">
                            <h4>Theme</h4>
                            <p>Dark Mode</p>
                        </div>

                        <div className="setting-card">
                            <h4>Accent Color</h4>
                            <div className="color-preview"></div>
                        </div>
                    </>
                )}

                {tab==="voice" && (
                    <>
                        <h2>Voice</h2>

                        <div className="setting-card">
                            <h4>Voice</h4>
                            <div className="voice-dropdown">

                        <button
                            className="voice-dropdown-btn"
                            onClick={() => setOpenVoice(!openVoice)}
                        >
                            <div className="voice-selected">

                                <Mic size={18}/>

                                <span>{voice}</span>

                            </div>

                            <ChevronDown
                                size={18}
                                className={openVoice ? "rotate" : ""}
                            />

                        </button>

                        {openVoice && (

                            <div className="voice-menu">

                                {voices.map((v) => (

                                    <button
                                        key={v}
                                        className={`voice-item ${
                                            voice === v ? "active" : ""
                                        }`}
                                        onClick={() => {

                                            setVoice(v);

                                            localStorage.setItem("voice", v);

                                            setOpenVoice(false);

                                        }}
                                    >

                                        <div className="voice-item-left">

                                            <Mic size={16}/>

                                            {v}

                                        </div>

                                        {voice === v && <Check size={16}/>}

                                    </button>

                                ))}

                            </div>

                        )}

                    </div>
                           
                        </div>

                        <div className="setting-card">
                            <h4>Volume</h4>
                            <input type="range"/>
                        </div>
                    </>
                )}

                {tab==="memory" && (
                    <>
                        <h2>Memory</h2>

                        <div className="setting-card">
                            <h4>Memory Status</h4>
                            <p>Enabled</p>
                        </div>

                        <div className="setting-card">
                            <button

                                className="purple-btn"

                                onClick={() => setShowMemory(true)}

                            >

                                Manage Memory

                            </button>
                        </div>
                    </>
                )}

                {tab==="model" && (
                    <>
                        <h2>LLM Model</h2>

                        <div className="setting-card">
                            <h4>Current Model</h4>
                            <p>minimax-m3:cloud</p>
                        </div>
                    </>
                )}

                {tab==="account" && (
                    <>
                        <h2>Account</h2>

                        <div className="setting-card">
                            <h4>Subscription</h4>
                            <p>FREE PLAN</p>
                        </div>
                    </>
                )}

                {tab==="about" && (
    <>

        <h2>Isekai Gate System</h2>


        <div className="setting-card">

            <h4>Version</h4>

            <p>
                v1.0 Beta
            </p>

        </div>



        <div className="setting-card">

            <h4>About</h4>

            <p>
                Aoi is an AI companion
                designed for natural conversation,
                voice interaction, and personalized experience.
            </p>

        </div>



        <div className="setting-card">

            <h4>Technology</h4>

            <p>
                React • FastAPI • Gemini • PostgreSQL • Ollama • Live2D
            </p>

        </div>



        <div className="setting-card">

            <h4>Status</h4>

            <p className="online-text">

                <span className="status-green">●</span>

                Online System

            </p>

        </div>

        
    </>
)}

               

            {

            showMemory && (

                <div className="memory-popup">

                    <div className="memory-container">

                        <button

                            className="close-btn"

                            onClick={() => setShowMemory(false)}

                        >

                            ✕

                        </button>

                        <ManageMemory/>

                    </div>

                </div>

            )

        }

            </div>

            {showAdminDenied && (

            <div className="admin-popup-overlay">

                <div className="admin-popup">

                    <div className="admin-popup-icon">
                        🛡
                    </div>

                    <h2>Admin Dashboard</h2>

                    <div className="admin-popup-log">

                        <p>━━━━━━━━━━━━━━━</p>

                        <p>🔄 Menghubungi server...</p>

                        <p className="success">
                            ✔ Identitas ditemukan
                        </p>

                        <p className="failed">
                            ❌ Otoritas Admin tidak ditemukan
                        </p>

                    </div>

                    <div className="admin-popup-status">

                        <span>Status</span>

                        <strong>
                            Masih menjadi rakyat biasa.
                        </strong>

                    </div>

                    <button
                        className="admin-popup-btn"
                        onClick={() => setShowAdminDenied(false)}
                    >
                        Mengerti
                    </button>

                </div>

            </div>

            )}

        </div>

    );

}

