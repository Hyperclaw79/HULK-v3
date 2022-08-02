module.exports = {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    webpack: (defaultConfig, env) =>
        Object.assign(defaultConfig, {
            entry: {
                background: './main/background.ts',
                preload: './main/preload.ts',
            },
        }),
};