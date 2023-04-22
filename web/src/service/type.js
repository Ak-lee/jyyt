import {get, post, del, put} from '@/utils/request'


const baseUrl = '/api/tasktype';


export const table = function (curPage, size, key) {
    let params = {
        curPage,
        size
    }
    if (key != null) {
        params.key = key;
    }
    return get(`${baseUrl}/table`, params);
}

export const tableAll = function () {
    return get(`${baseUrl}/tableAll`);
}

export const getWithTasktypeDetail = function () {
    return get(`${baseUrl}/getWithTasktypeDetail`);
}

export const getById = function (id) {
    return get(`${baseUrl}/info/${id}`)
}

export const byTasktypeId = function (taskTypeId) {
    let params = {
        taskTypeId,
    }
    return get(`${baseUrl}/byTasktypeId`, params);
}

export const add = function (body) {

    return post(`${baseUrl}`, body);
}

export const update = function (body) {
    return put(`${baseUrl}`, body);
}

export const updateDetail = function (body) {
    put(`${baseUrl}/updateDetail`, body);
}

export const removeById = function (id) {
    return del(`${baseUrl}/${id}`)
}


