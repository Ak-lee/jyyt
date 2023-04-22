/**
 * axios做二次封装
 */
//@ts-nocheck
import {ElMessage, ElLoading} from 'element-plus';
import {nextTick} from 'vue';
import instance from './instance'


/**
 * 统一处理http请求
 * @param url 接口
 * @param method 请求方式  get|post|put|delete
 * @param params 参数
 */
function request(url, method, params) {

    return new Promise((resolve, reject) => {

        let silent = method.startsWith('silent');
        let l_inst;
        if (silent) {
            method = method.substring(6);
        } else {
            l_inst = ElLoading.service()
        }
        let data = {}
        if (params) {
            // get直接发就行
            if (method == 'get') data = {params}
            // post请求要用data字段放到请求体里面
            if (method == 'post' || method == 'put' || method == 'delete') data = {data: params}
        }

        instance({
            url,
            method,
            ...data
        }).then((res) => {
            if (!res.code) {
                resolve(res)
            } else {
                if (res.code === 1) {
                    resolve(res.data);
                } else {
                    resolve(res);
                }
            }
        }).catch((error) => {
            ElMessage.error(error.message)
        }).finally(() => {
            if (!silent) {
                nextTick(() => {
                    l_inst.close()
                })
            }
        })
    })
}

export const get = function (url, params) {
    return request(url, 'get', params)
}

export const post = function (url, params) {
    return request(url, 'post', params)
}

export const put = function (url, params) {
    return request(url, 'put', params)
}

export const del = function (url, params) {
    return request(url, 'delete', params)
}

export const silentGet = function (url, params) {
    return request(url, 'silentget', params)
}

export const silentPost = function (url, params) {
    return request(url, 'silentpost', params)
}