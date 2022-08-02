/** This module facilitates the communication with Hulk Server
via a Named Pipe. */

import * as net from 'net';

import { contextBridge, ipcRenderer } from "electron";

import { StatusCodes, Messages, ClientCommands } from "../types/enums.d";
import { BotnetProps } from "../types/props.d";

import { MessageData } from '../types/bridge.d';

// Flag to prevent multiple instances of the pipe
let PIPE_INITIATED = false;

let PIPE_NAME = "HULK";

// Platform specific Named Pipe
PIPE_NAME = process.platform === 'win32'
    ? `\\\\.\\pipe\\${PIPE_NAME}`
    : `/tmp/${PIPE_NAME}`;

// Regex to extract data from the logs
const botPatten = new RegExp([
    /(?<message>Data|Status|Target|Error){1}.*/,
    /(?:<(?<data>.*?)>).+/,
    /\[(?:(?<botIp>.*):(?<botPort>.*))*?\]/
].map(r => r.source).join(''))

// Initialize the botnetData
const botnetData: BotnetProps = {
    target: {
        url: '',
        status: StatusCodes.NO_LUCK,
    },
    botList: [],
};

// The Pipe Monitor function
const monitor = (callbacks: { [key: string]: CallableFunction }) => {
    // Update the data for every command received
    const updateClient = (input: string) => {
        const result = botPatten.exec(input);
        if (!result || !result.groups) { return; }
        const data: MessageData = {
            message: result.groups.message,
            data: result.groups.data,
            botIp: result.groups.botIp,
            botPort: parseInt(result.groups.botPort)
        };
        // Find the bot in the botnetData if it exists
        const bot = botnetData.botList.find(
            b => b.ip === data.botIp
                && b.port === data.botPort
        );

        switch (data.message) {
            // If a Send Target message is received, update the target.
            case Messages.TARGET:
                botnetData.target = {
                    url: data.data,
                    status: StatusCodes.NO_LUCK
                };
                break;
            // If a Data message is received, update the bot's status
            case Messages.DATA:
                switch (data.data) {
                    // Add new bots to the botnetData
                    case ClientCommands.SEND_TARGET || ClientCommands.STANDBY:
                        if (!bot) {
                            botnetData.botList.push({
                                ip: data.botIp,
                                port: data.botPort,
                                status: "online",
                                targetStatus: StatusCodes.NO_LUCK
                            });
                        }
                        else {
                            bot.status = "online";
                        }
                        if (data.data === ClientCommands.SEND_TARGET) {
                            botnetData.target.status = StatusCodes.NO_LUCK;
                        }
                        break;
                    // Set the bot's status to offline
                    case ClientCommands.KILLED || ClientCommands.ERROR:
                        if (bot) {
                            bot.status = "offline";
                        }
                        break;
                }
                break;
            // If a Status message is received, update the Target's status
            // and the bot's target status.
            case Messages.STATUS:
                if (botnetData.target.status !== StatusCodes.PWNED) {
                    botnetData.target.status = StatusCodes[
                        data.data.replace(
                            'StatusCodes.', ''
                        ) as keyof typeof StatusCodes
                    ];
                }
                if (bot) {
                    bot.targetStatus = StatusCodes[
                        data.data.replace(
                            'StatusCodes.', ''
                        ) as keyof typeof StatusCodes
                    ];
                }
                break;
            // If a Connection Error message is received, set the bot's status to Offline
            case Messages.ERROR:
                if (bot) {
                    bot.status = "offline";
                }
        }
    };

    if (PIPE_INITIATED) {
        // If the pipe has already been initiated,
        // just return the updated data.
        return botnetData;
    }

    // Create a new Named Pipe
    const server = net.createServer((stream: net.Socket) => {

        stream.on('connection', () => {
            console.log('Connection established');
            if (callbacks?.onConnection) {
                callbacks.onConnection();
            }
        });

        // Split the named pipe data steam into commands.
        stream.on('data', (c: string) => {
            const input = c.toString();
            // Regex for commands.
            input.split(/\|(.+?)\|/).filter(
                Boolean
            ).forEach(updateClient);
            if (callbacks?.onData) {
                callbacks.onData(botnetData);
            }
        });

        stream.on('error', (error: string) => {
            console.log('Something went wrong');
            if (callbacks?.onError) {
                callbacks.onError(error);
            }
        });

        stream.on('end', () => {
            console.log('Connected lost with Hulk Server');
            server.close();
            if (callbacks?.onDisconnect) {
                callbacks.onDisconnect();
            }
        });
    });

    // Start the listener on the Named Pipe
    server.listen(PIPE_NAME, () => {
        PIPE_INITIATED = true;
        console.log(`Listening for Messages on [${PIPE_NAME}]...\n`);
    });
}

// Export the Pipe Monitor function to the frontend.
contextBridge.exposeInMainWorld("electronAPI", {
    piper: {
        "monitor": (callbacks: { [key: string]: CallableFunction }) => {
            monitor(callbacks);
        }
    },
    reload: () => ipcRenderer.send('request-reload')
});
