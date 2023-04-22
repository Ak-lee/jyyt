import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/calendar';


export const table = function (lineId, curPage, size) {
    let params = {
        curPage,
        size,
        lineId
    }
    return get(`${baseUrl}/table`, params)
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

export const getItem = function (lineId, date) {
    let params = {
        lineId,
        date
    }
    return get(`${baseUrl}/getItem`, params);
}

export const add = function (body) {
    return post(`${baseUrl}/`, body);
}


export const update = function (body) {
    return put(`${baseUrl}/`, body);
}

export const removeById = function (id) {
    return del(`${baseUrl}/${id}`)
}
