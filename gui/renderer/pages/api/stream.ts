/** Fallback API if Electron is not available.
Refer ../main/preload.ts for docs. */

import * as net from 'net';

import { StatusCodes, Messages, ClientCommands } from "../../types/enums.d";
import { BotnetProps } from "../../types/props.d";

import { MessageData } from '../../types/bridge.d';
import { NextApiRequest, NextApiResponse } from 'next/types';

let PIPE_INITIATED = false;

let PIPE_NAME = "HULK";
PIPE_NAME = process.platform === 'win32'
    ? `\\\\.\\pipe\\${PIPE_NAME}`
    : `/tmp/${PIPE_NAME}`;

const botPatten = new RegExp([
    /(?<message>Data|Status|Target|Error){1}.*/,
    /(?:<(?<data>.*?)>).+/,
    /\[(?:(?<botIp>.*):(?<botPort>.*))*?\]/
].map(r => r.source).join(''))

const botnetData: BotnetProps = {
    target: {
        url: '',
        status: StatusCodes.NO_LUCK,
    },
    botList: [],
};

const monitor = (callbacks: { [key: string]: CallableFunction }) => {
    const updateClient = (input: string) => {
        const result = botPatten.exec(input);
        if (!result || !result.groups) { return; }
        const data: MessageData = {
            message: result.groups.message,
            data: result.groups.data,
            botIp: result.groups.botIp,
            botPort: parseInt(result.groups.botPort)
        };
        const bot = botnetData.botList.find(
            b => b.ip === data.botIp
                && b.port === data.botPort
        );
        switch (data.message) {
            case Messages.TARGET:
                botnetData.target = {
                    url: data.data,
                    status: StatusCodes.NO_LUCK
                };
                break;
            case Messages.DATA:
                switch (data.data) {
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
                    case ClientCommands.KILLED || ClientCommands.ERROR:
                        if (bot) {
                            bot.status = "offline";
                        }
                        break;
                }
                break;
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
            case Messages.ERROR:
                if (bot) {
                    bot.status = "offline";
                }
        }
    };

    if (PIPE_INITIATED) {
        return botnetData;
    }
    const server = net.createServer((stream: net.Socket) => {

        stream.on('connection', () => {
            console.log('Connection established');
            if (callbacks?.onConnection) {
                callbacks.onConnection();
            }
        });

        stream.on('data', (c: string) => {
            const input = c.toString();
            input.split(/\|(.+?)\|/).filter(
                Boolean
            ).forEach(updateClient);
            botnetData.botList.forEach((bot, idx) => {
                bot.avatar = `/robots/${Math.round(idx % 9)}.png`;
            });
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

    server.listen(PIPE_NAME, () => {
        PIPE_INITIATED = true;
        console.log('Listening for Messages...\n');
    });
}

const handler = async(req: NextApiRequest, res: NextApiResponse) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache, no-transform');
    res.setHeader('Connection', 'keep-alive');
    res.end(`data: ${JSON.stringify(botnetData)}\n\n`);
};

monitor({
    onData: console.log,
    onConnection: console.log,
    onError: console.error,
    onDisconnect: console.log
});

export default handler;