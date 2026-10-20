import { useEffect, useState } from "react";

import "./Live.css";

import AvatarStageLive from "../AvatarStageLive";

import { API_URL } from "../../config";
export default function Live({ user, onExit }) {


    const [status, setStatus] = useState(
        "Connecting..."
    );


    const [viewer, setViewer] = useState(0);


    const [likes, setLikes] = useState(0);


    const [gifts, setGifts] = useState([]);


    const [comments, setComments] = useState([]);


    const [queue, setQueue] = useState([]);

    const [username, setUsername] = useState("kuroaidev");

    const connectLive = async () => {
        try {

            await fetch(`${API_URL}/live/connect`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization:
                        `Bearer ${localStorage.getItem("token")}`
                },
                body: JSON.stringify({
                    username
                })
            });

        } catch (e) {
            console.log(e);
        }
    };

    const disconnectLive = async () => {

        try {

            await fetch(`${API_URL}/live/disconnect`, {
                method: "POST",
                headers: {
                    Authorization:
                        `Bearer ${localStorage.getItem("token")}`
                }
            });

        } catch (e) {
            console.log(e);
        }

    };

    const loadStatus = async () => {

        try {

            const res = await fetch(
                `${API_URL}/live/status`,
                {
                    headers: {
                        Authorization:
                            `Bearer ${localStorage.getItem("token")}`
                    }
                }
            );

            const data = await res.json();

            console.log(data);

        } catch (e) {
            console.log(e);
        }

    };

    useEffect(()=>{


        const ws = new WebSocket(
            "ws://localhost:8000/live/ws"
        );



        ws.onopen = ()=>{


            console.log(
                "WEBSOCKET CONNECTED"
            );


            setStatus(
                "Connected"
            );


        };




       ws.onmessage = (event)=>{


                const data =
                    JSON.parse(event.data);

                console.log(
                    "MESSAGE MASUK"
                );

                console.log(
                    "LIVE DATA:",
                    data
                );


                if(data.type === "ai_reply"){

                const audioUrl =
                    `${API_URL}/${data.audio}`;

                const audio = new Audio(audioUrl);

                audio.volume = 1.0;

                audio.play().catch(err => {
                    console.log(
                        "Audio gagal diputar:",
                        err
                    );
                });


                if(window.live2dModel){

                    window.live2dModel.startLipSync(
                        audioUrl
                    );

                }

            }
              

            if(data.comment){



                const comment = {


                    username:
                        data.user,


                    message:
                        data.comment,


                    id:
                        data.unique_id


                };




                setComments(prev=>[

                    comment,

                    ...prev.slice(0,49)

                ]);




                setQueue(prev=>[

                    comment,

                    ...prev

                ]);



            }



        };




        ws.onerror = (error)=>{


            console.log(
                "WEBSOCKET ERROR",
                error
            );


            setStatus(
                "Error"
            );


        };




        ws.onclose = ()=>{


            console.log(
                "WEBSOCKET CLOSED"
            );


            setStatus(
                "Disconnected"
            );


        };





        return ()=>{


            ws.close();


        };



    },[]);







    return (

        <div className="live-page">


            <header className="live-header">


                <div className="live-logo">

                    Isekai Live

                </div>



                <div className="live-user">


                    <span>

                        {user?.username ?? "Guest"}

                    </span>



                    <button

                        className="exit-live-btn"

                        onClick={onExit}

                    >

                        Exit Live

                    </button>


                </div>



            </header>






            <main className="live-content">



                <section className="live-avatar">


                    <AvatarStageLive />


                </section>






                <aside className="live-side">





                    <div className="live-card">

                    <h3>TikTok Live</h3>

                    <input
                        value={username}
                        onChange={(e)=>setUsername(e.target.value)}
                        placeholder="TikTok Username"
                    />

                    <div className="live-control-buttons">

                        <button
                            className="connect-btn"
                            onClick={connectLive}
                        >
                            Connect
                        </button>

                        <button
                            className="disconnect-btn"
                            onClick={disconnectLive}
                        >
                            Disconnect
                        </button>

                    </div>

                    <div
                        className={`live-status ${
                            status === "Connected"
                                ? "connected"
                                : ""
                        }`}
                    >
                        <div className="live-status-dot"></div>

                        <span>{status}</span>

                    </div>

                </div>






                    <div className="live-card">


                        <h3>
                            Viewer
                        </h3>


                        <p>

                            👥 {viewer}

                        </p>


                    </div>







                    <div className="live-card">


                        <h3>
                            Likes
                        </h3>


                        <p>

                            ❤️ {likes}

                        </p>


                    </div>







                    <div className="live-card">


                        <h3>
                            Gifts
                        </h3>


                        {

                            gifts.length === 0

                            ?

                            <p>
                                No gifts
                            </p>

                            :

                            gifts.map(
                                (gift,index)=>(

                                    <div key={index}>

                                        🎁 {gift}

                                    </div>

                                )
                            )

                        }


                    </div>








                    <div className="live-card comment-card">


                        <h3>
                            Comment Queue
                        </h3>




                        <div className="comment-list">


                            {

                            comments.length === 0

                            ?

                            <p>
                                Waiting comment...
                            </p>


                            :


                            comments.map(
                                (item,index)=>(


                                    <div key={index}>


                                        💬

                                        <b>
                                            {item.username}
                                        </b>


                                        :

                                        {item.message}


                                    </div>


                                )
                            )


                            }



                        </div>



                    </div>






                </aside>



            </main>




        </div>

    );

}