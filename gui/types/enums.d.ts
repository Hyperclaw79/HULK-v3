/**
 * @readonly Client Commands
 * @enum {string}
 * @property {string} ERROR
 * @property {string} KILLED
 * @property {string} STANDBY
 * @property {string} SEND_TARGET
 * @property {string} READ_STATUS
 */
 export enum ClientCommands {
    ERROR = 'ClientCommands.ERROR',
    KILLED = 'ClientCommands.KILLED',
    STANDBY = 'ClientCommands.STANDBY',
    SEND_TARGET = 'ClientCommands.SEND_TARGET',
    READ_STATUS = 'ClientCommands.READ_STATUS'
}

/**
 * @readonly Status Codes
 * @enum {string}
 * @property {string} CONNECTION_FAILURE
 * @property {string} NO_LUCK
 * @property {string} ANTI_DDOS
 * @property {string} FORBIDDEN
 * @property {string} NOT_FOUND
 * @property {string} PWNED
 */
export enum StatusCodes {
    CONNECTION_FAILURE = 'StatusCodes.CONNECTION_FAILURE',
    NO_LUCK = 'StatusCodes.NO_LUCK',
    ANTI_DDOS = 'StatusCodes.ANTI_DDOS',
    FORBIDDEN = 'StatusCodes.FORBIDDEN',
    NOT_FOUND = 'StatusCodes.NOT_FOUND',
    PWNED = 'StatusCodes.PWNED'
}

/**
 * @readonly Messages
 * @enum {string}
 * @property {string} DATA
 * @property {string} STATUS
 * @property {string} TARGET
 * @property {string} COMMAND
 * @property {string} ERROR
 */
export enum Messages {
    DATA = 'Data',
    STATUS = 'Status',
    TARGET = 'Target',
    COMMAND = 'Command',
    ERROR = 'Error'
}

/**
 * @readonly Error Messages
 * @enum {string}
 * @property {string} CONNECTION_ABORTED
 * @property {string} CONNECTION_REFUSED
 * @property {string} CONNECTION_RESET
 */
export enum ErrorMessage {
    CONNECTION_ABORTED = 'ErrorMessages.CONNECTION_ABORTED',
    CONNECTION_REFUSED = 'ErrorMessages.CONNECTION_REFUSED',
    CONNECTION_RESET = 'ErrorMessages.CONNECTION_RESET'
}
