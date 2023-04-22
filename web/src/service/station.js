import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/station';


export const table = function (lineId, curPage, size) {
    let params = {
        curPage,
        size
    }
    return get(`${baseUrl}/table/${lineId}`, params)
}

export const tableAll = function (curPage, size) {
    let params = {
        curPage,
        size
    }
    return get(`${baseUrl}/table`, params);
}

export const getById = function (id) {
    return get(`${baseUrl}/info/${id}`)
}

export const add = function (body) {
    return post(`${baseUrl}/`, body);
}


export const update = function (body) {
    return put(`${baseUrl}/`, body);
}

export const removeById = function (id) {
    return del(`${baseUrl}/${id}/`)
}
