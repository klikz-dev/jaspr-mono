module.exports = function (api) {
    api.cache(true);
    return {
        presets: ['babel-preset-expo'],
        plugins: [
            'react-native-classname-to-style',
            ['react-native-platform-specific-extensions', { extensions: ['scss', 'css'] }],
            [
                'module-resolver',
                {
                    alias: {
                        config: './src/config',
                        assets: './src/assets',
                        jah: './src/jah',
                        lib: './src/lib',
                        state: './src/state',
                        pages: './src/pages',
                        components: './src/components',
                    },
                },
            ],
            'react-native-reanimated/plugin',
        ],
    };
};
