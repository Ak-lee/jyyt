import {get, post, del, put} from '@/utils/request'


const baseUrl = '/api/lastRespairs';


export const table = function (pageNum, pageSize,key) {
    let params = {
        pageNum,
        pageSize
    }
    if (key != null) {
        params.key = key;
    }
    return get(`${baseUrl}/table`, params);
}

export const getById = function (id) {
    return get(`${baseUrl}/info/${id}`)
}

export const add = function (body) {

    return post(`${baseUrl}`, body);
}


export const update = function (body) {
    return put(`${baseUrl}`, body);
}

export const removeById = function (id) {

    return del(`${baseUrl}/info/${id}`)
}

export const getlastRepairs = function (lineId ,curPage,size ) {
    let params = {
        lineId,
        curPage,
        size
    }
    return get(`${baseUrl}/getlastRepairs`, params);
}