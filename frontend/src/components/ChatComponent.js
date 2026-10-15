import React, {useEffect, useRef, useState} from 'react';
import {socketService} from "../services/socketService";
import {client} from "websocket";

const ChatComponent = () => {
    const [room, setRoom] = useState(null)
    const [targetUser, setTargetUser] =useState(null)
    const [socketClient, setSocketClient] = useState(null)
    const [messages, setMessages] = useState([])
    const [currentUserId, setCurrentUserId] = useState(null)
    const roomInput = useRef()
    useEffect(() => {
        if (room) {
            socketInit(room).then(client => setSocketClient((client)))

        }
        return()=>{
            if(client){
                client.close();
            }
        };
    }, [room])

    const socketInit = async (room) => {
        const {chat} = await socketService();
        const client = await chat(room)

        client.onopen = () => {
            console.log('chat is connected')
        }
        client.onmessage=({data})=>{//отримаємо від беку юзера name i id,message
            const{type, userId, message, is_private, room: privateRoom, user}=JSON.parse(data.toString());
             if (type === 'current_user') {
        setCurrentUserId(userId)
        return
    }
             if (user && user.includes('_')) {
                const [userId, username] = user.split('_'); setMessages(prevState => [...prevState,
                     {userId,
                         username,
                         message,
                         is_private,
                         room: privateRoom
                     }])
            } else {

                setMessages(prevState => [...prevState, {user, message}])
            }
        }


        return client
    }
     const roomHandler =()=>{
        setRoom(roomInput.current.value)
    }

    const handleEnterKey = (e) => {
        console.log('SENDING:', {
    targetUser,
    action: targetUser ? 'send_private_message' : 'send_message',
    text: e.target.value
})
        if (e.key === 'Enter') {
            socketClient.send(JSON.stringify({
                data: targetUser?{text:`Private ${e.target.value}`,userId:targetUser}:{ text:e.target.value},
                action: !targetUser?'send_message':'send_private_message',
                request_id: new Date().getTime()
            }))
            e.target.value = ''
        }
    }

    return (
        <div>
            {
                !room
                ?
                    <div>
                        <input type="text" ref={roomInput}/>
                        <button onClick={roomHandler}>Go to room</button>
                    </div>
                    :
                    <div>
                        {messages.map(msg=>
                            <div>
                                <span onClick={()=>{
                                    console.log('CLICKED MESSAGE:', msg)
                                    if (!msg.userId || String(msg.userId) === String(currentUserId)) return
                                    if(!targetUser){
                                        setTargetUser(msg.userId)
                                    }

                                }
                                }>{msg.username||msg.userId||msg.user}</span>: {msg.message}
                        </div>)}
                         {targetUser && (
                            <p>
                                Private chat with user ID: {targetUser}
                                <button onClick={() => setTargetUser(null)}>
                                    Back to general chat
                                </button>
                            </p>
                        )}
                        <input type="text" onKeyDown={handleEnterKey}/>
                    </div>
            }
        </div>
    );

};

export {ChatComponent}