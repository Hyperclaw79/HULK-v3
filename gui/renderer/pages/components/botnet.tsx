/** A component to encapsulate the Botnet */

import { useState, useEffect } from "react";

import Target from "./target";
import Bot from "./bot";

import { BotnetProps } from "../../types/props.d";
import { StatusCodes } from "../../types/enums.d";

const Botnet = () => {
    // Initialize the state of the Botnet.
    const [data, setData] = useState<BotnetProps>({
        target: {
            url: "",
            status: StatusCodes.NO_LUCK
        },
        botList: []
    });

    useEffect(() => {
        const updateBotnet = (botData: BotnetProps) => {
            // Assign a random avatar for each bot.
            botData.botList.forEach((bot, idx) => {
                bot.avatar = `/robots/${Math.round(idx % 9)}.png`;
            });
            setData(botData);
        }
        let source: EventSource;
        /* If running the code within Electron, we can access the Pipe Monitor
        from the electronAPI bridge. */
        if (window.electronAPI) {
            const piper = window.electronAPI.piper;
            const reload = window.electronAPI.reload;
            piper.monitor({
                onConnection: console.log,
                onError: console.error,
                onDisconnect: reload,
                // On receiving a message, update the state of the Botnet.
                onData: updateBotnet
            });
        }
        // Otherwise, we can can get the data from a HTTP Server-Sent Events (SSE) stream.
        else {
            alert("Electron API is not available");
            // Create an EventSource to listen to the HTTP Stream.
            source = new EventSource("http://localhost:3000/api/stream");
            source.onmessage = (event) => {
                // On receiving a message, update the state of the Botnet.
                const parsed: BotnetProps = JSON.parse(event.data);
                updateBotnet(parsed);
            }
        }
        return () => {
            if (source) {
                source.close();
                window.location.reload();
            }
        }
    }, []);

    return (
        <div className="botnet">
            <div className="target">
                <Target
                    url={data.target.url}
                    status={data.target.status}
                />
            </div>
            <div className="botlist">
                {data.botList.map(
                    (bot, index) => <Bot key={index} {...bot} />
                )}
            </div>
        </div>
    );
}

export default Botnet;
