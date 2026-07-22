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
                    "LIVE DATA:",
                    data
                );



                if(data.type === "ai_reply"){


                    const audioUrl =
                        `${API_URL}/${data.audio}`;

                    audio.play();

                     // gunakan sistem lip sync yang sama

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


                        <h3>
                            TikTok Status
                        </h3>


                        <p>

                            🟢 {status}

                        </p>


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