module.exports = function (api) {
    api.cache(true);
    return {
        plugins: [
            [
                'module-resolver',
                {
                    alias: {
                        assets: './src/assets',
                        lib: './src/lib',
                        state: './src/state',
                        components: './src/components',
                    },
                },
            ],
        ],
    };
};
