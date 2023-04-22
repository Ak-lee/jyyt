const {defineConfig} = require('@vue/cli-service')
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const {ElementPlusResolver} = require('unplugin-vue-components/resolvers')


const path = require("path");

function resolve(dir) {
    return path.join(__dirname, dir);
}

let proxyObj = {};


proxyObj['/api'] = {
    // websocket
    ws: false,
    target: 'http://localhost:8880',
    changeOrigin: true,
    pathRewrite: {
        '^/api': ""
    }
}

module.exports = defineConfig({
    chainWebpack: config => {
        config.resolve.alias
            .set("@", resolve("src"));
        config.module
            .rule('vue')
            .use('vue-loader')
            .tap((options) => {
                return {
                    ...options,
                    reactivityTransform: true
                }
            })
        config.plugin('html')
            .tap(args => {
                args[0].title = "城轨列车检运一体化系统"
                return args;
            })
    },
    // transpileDependencies: true,
    devServer: {
        host: '0.0.0.0',
        port: 8080,
        proxy: proxyObj
    },
    lintOnSave: false,
    configureWebpack: {
        plugins: [
            AutoImport({
                resolvers: [ElementPlusResolver({
                    importStyle: false
                })]
            }),
            Components({
                resolvers: [ElementPlusResolver({
                    importStyle: false
                })]
            }),
        ],
    },
})

