import { useState } from "react";
import {
    Settings,
    Palette,
    Mic,
    Brain,
    Cpu,
    User,
    Info
} from "lucide-react";

import "./SettingsPage.css";
import ManageMemory from "./settings/ManageMemory";


export default function SettingsPage(){

    const [tab,setTab]=useState("general");
    const [voice,setVoice]=useState(

    localStorage.getItem("voice") ||

    "Leda"

);
    const [showMemory,setShowMemory]=useState(false);
    const [style,setStyle] = useState(
    localStorage.getItem("style") || ""
);



    return(

        <div className="settings-page">

            <div className="settings-sidebar">

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

            </div>

            <div className="settings-content">

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

                            <select
                                className="voice-select"
                                value={voice}
                                onChange={(e)=>{

                                    setVoice(e.target.value);

                                    localStorage.setItem(
                                        "voice",
                                        e.target.value
                                    );

                                }}
                            >

                            <option>Despina</option>
                            <option>Aoede</option>
                            <option>Kore</option>
                            <option>Puck</option>
                            <option>Leda</option>
                            <option>Charon</option>

                            </select>
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

        </div>

    );

}

