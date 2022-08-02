/** A component to display the Online/Offline Status message. */

import { StatusCodes } from "../../types/enums.d";

/**
 * @readonly StatusColors
 * @enum {string}
 * @property {string} GREEN - The color of the status message when the website is taken down.
 * @property {string} RED - The color of the status message when the website cannot be DDoSed.
 * @property {string} YELLOW - The color of the status message when the website is unknown.
 * @property {string} WHITE - The color of the status message when the website is online.
 */
export enum StatusColors {
    GREEN = 'rgb(112, 255, 77)',
    RED = 'rgb(233, 41, 41)',
    YELLOW = 'rgb(248, 188, 23)',
    WHITE = 'rgb(255, 255, 255)'
}

/**
 * @readonly statusLevelMap
 * Map of the status codes to the color of the status message.
 * @property {StatusCodes} [StatusCodes.NO_LUCK]
 * @property {StatusCodes} [StatusCodes.PWNED]
 * @property {StatusCodes} [StatusCodes.ANTI_DDOS]
 * @property {StatusCodes} [StatusCodes.FORBIDDEN]
 * @property {StatusCodes} [StatusCodes.NOT_FOUND]
 * @property {StatusCodes} [StatusCodes.CONNECTION_FAILURE]
 * @property {string} UNKNOWN
 */
export const statusLevelMap = {
    [StatusCodes.NO_LUCK]: StatusColors.YELLOW,
    [StatusCodes.PWNED]: StatusColors.GREEN,
    [StatusCodes.ANTI_DDOS]: StatusColors.RED,
    [StatusCodes.FORBIDDEN]: StatusColors.RED,
    [StatusCodes.NOT_FOUND]: StatusColors.RED,
    [StatusCodes.CONNECTION_FAILURE]: StatusColors.RED,
    'UNKNOWN': StatusColors.WHITE,
    undefined: StatusColors.WHITE
}

/**
 * @interface StatusProps
 * @property {string} status - The status code of the website.
 * @property {string} level - The color of the status message.
 */
export interface StatusProps {
    status: string;
    level: StatusColors;
}

const Status = ({ status, level }: StatusProps) => {

    return (
        <div className="statusContainer">
            <svg
                width={20} height={20}
                viewBox="0 0 40 40"
            >
                <circle
                    cx={20} cy={20}
                    r={20} stroke="black"
                    strokeWidth={3}
                    fill={level}
                />
            </svg>
            <span>{(status || StatusCodes.NO_LUCK).toUpperCase()}</span>
        </div>
    );
}

export default Status;