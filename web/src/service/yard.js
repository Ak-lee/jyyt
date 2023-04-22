import {get, post, del, put} from '@/utils/request'


const baseUrl = '/api/yard';


export const table = function (curPage, size,key) {
    let params = {
        curPage,
        size
    }
    if (key != null) {
        params.key = key;
    }
    return get(`${baseUrl}/table`, params);
}

export const getById = function (id) {
    return get(`${baseUrl}/info/${id}`)
}

export const getByLineId = function(lineId) {
    let params = {
        lineId
    }
    return get(`${baseUrl}/list`, params);
}

export const add = function (body) {

    return post(`${baseUrl}`, body);
}


export const update = function (body) {
    return put(`${baseUrl}`, body);
}

export const removeById = function (id) {

    return del(`${baseUrl}/${id}`)
}
