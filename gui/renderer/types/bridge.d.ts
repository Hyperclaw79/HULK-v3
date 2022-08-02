// Expose the Pipe Monitor as a bridge to Frontend
export type electronAPI = {
    piper: {
        monitor: (callbacks: { [key: string]: CallableFunction }) => void;
    }
    reload: () => void;
}

// Parsed Message Data
export type MessageData = {
    message: string,
    data: string,
    botIp: string,
    botPort: number
};

// Expose the bridge to global window
declare global {
    interface Window {
        electronAPI: electronAPI;
    }
}
