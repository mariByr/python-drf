import React, {useEffect, useState} from 'react';
import {pizzasService} from "../services/pizzasService";
import {socketService} from "../services/socketService";
import PizzaComponent from "./PizzaComponent";

const PizzasComponent = () => {
    const [pizzas,setPizzas]=useState([])
    const[trigger,setTrigger]=useState(null)
    useEffect(() => {
        pizzasService.getAll().then(({data})=>setPizzas(data.data))
    }, [trigger]);
    useEffect(() => {
        socketInit().then()
    }, []);
    //  витягуємо з сокет сервісу функцію для створення вебсокету з піцами, і запускаємрц ю функцію тобто створюємо клієнт тобто сокет ззєднання
    const socketInit = async()=>{
        const {pizzas}=await socketService()
        const client= await pizzas()
        client.onopen=()=>{
            console.log('Pizza socket connected')
            client.send(JSON.stringify({
                action:'subscribe_to_pizza_model_changes',
                request_id:new Date().getTime()
                            }))
        }
        //onmessage ми отримали повідомлення по вебсокету від беккенду бо є постійний звязок і підписка на повідомлееня від обзьорвера
        client.onmessage=({data})=>{
            setTrigger(prev => !prev)}//взяти поперпеднє і встановити протилежне
    }
    return (
        <div>
            {pizzas.map(pizza => <PizzaComponent key={pizza.id} pizza={pizza}/>)}
        </div>
    );
};

export default PizzasComponent;