import { useEffect, useState } from "react";

import {

    getMemories,
    createMemory,
    updateMemory,
    deleteMemory,
    deleteAllMemories

} from "../../api/memory";

import "./ManageMemory.css";

export default function ManageMemory(){

    const [memories,setMemories]=useState([]);

    const [showAdd,setShowAdd]=useState(false);

    const [editMemory,setEditMemory]=useState(null);

    const [deleteItem,setDeleteItem]=useState(null);

    const [memoryKey,setMemoryKey]=useState("");

    const [memoryValue,setMemoryValue]=useState("");

    useEffect(()=>{

        loadMemories();

    },[]);

    async function loadMemories(){

        const data=await getMemories();

        setMemories(data);

    }

    return(

        <div className="manage-memory">

            <h2>Manage Memory</h2>

            <p>
                Raphael remembers only the information you save.
            </p>

            <button

                className="add-memory-btn"

                onClick={()=>{

                    setMemoryKey("");

                    setMemoryValue("");

                    setShowAdd(true);

                }}

            >

                + Add Memory

            </button>

            <div className="memory-list">

                {memories.map(memory=>(

                    <div
                        className="memory-card"
                        key={memory.id}
                    >

                        <div className="memory-key">

                            {memory.memory_key}

                        </div>

                        <div className="memory-value">

                            {memory.memory_value}

                        </div>

                        <div className="memory-actions">

                            <button>✏</button>

                            <button>🗑</button>

                        </div>

                    </div>

                ))}

            </div>

        </div>

    );

}