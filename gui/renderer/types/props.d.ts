import { StatusCodes } from "./enums";

/**
 * @interface TargetProps
 * @property {string} url
 * @property {StatusCodes} status
 */
export interface TargetProps {
    url: string;
    status: StatusCodes;
}

/**
 * @interface BotProps
 * @property {string} ip
 * @property {number} port
 * @property {string} [avatar]
 * @property {string} status
 * @property {StatusCodes} [targetStatus]
 */
export interface BotProps {
    ip: string;
    port: number;
    avatar?: string;
    status: string;
    targetStatus?: StatusCodes;
}

/**
 * @interface BotnetProps
 * @property {TargetProps} target
 * @property {BotProps[]} botList
 */
export interface BotnetProps {
    target: TargetProps,
    botList: BotProps[];
}
