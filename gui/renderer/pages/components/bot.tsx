/** A component representing a Bot in the Hulk Botnet. */

import Status, { StatusColors, statusLevelMap } from "./status";
import { BotProps } from "../../types/props.d";

const Bot = (props: BotProps) => {
    return (
        <div
            className="bot"
            {
                ...(props.status === "offline"
                    ? {
                        style: {
                            opacity: 0.5,
                            filter: "drop-shadow(3px 3px 5px rgba(0, 0, 0, 0.5)) saturate(0.5)"
                        }
                    } : {}
                )
            }
        >
            <div className="left">
                <div className="botAvatar">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                        src={props.avatar || ''}
                        alt="avatar"
                        width={200} height={188}
                    />
                </div>
                <Status
                    status={props.status}
                    level={
                        props.status === 'online'
                        ? StatusColors.GREEN
                        : StatusColors.RED
                    }
                />
            </div>
            <div className="right">
                <div className="rightTop">
                    <div className="keys">
                        <div>HOST</div>
                        <div>PORT</div>
                    </div>
                    <div className="values">
                        <div className="botIp">
                            {props.ip}
                        </div>
                        <div className="botPort">
                            {props.port}
                        </div>
                    </div>
                </div>
                <div className="rightBottom">
                    Target Status:&nbsp;
                    <span style={{ color: statusLevelMap[props.targetStatus || 'UNKNOWN'] }}>
                        {
                            // Remove the StatusCodes. prefix from the status.
                            (props.targetStatus || 'UNKNOWN')
                            ?.replace(/StatusCodes\./, '')
                            ?.replace(/_/, ' ') || 'UNKNOWN'
                        }
                    </span>
                </div>
            </div>
        </div>
    );
}

export default Bot;