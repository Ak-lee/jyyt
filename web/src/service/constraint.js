import {get, post, del, put} from '@/utils/request'


const baseUrl = '/api/onedayMax';


export const table = function (lineId,pageNum, pageSize) {
    let params = {
        lineId,
        pageNum,
        pageSize,
    }
    // if (key != null) {
    //     params.key = key;
    // }
    return get(`${baseUrl}/table`, params);
}
export const tableAll = function (curPage, size) {
    let params = {
        curPage,
        size
    }
    return get(`${baseUrl}/tableAll`, params);
}

export const tableAllByLineId = function(lineId) {
    let params = {
        lineId
    }
    return get(`${baseUrl}/tableAllByLineId`, params);
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

export const getOnedayMax = function (lineId ,curPage,size ) {
    let params = {
        lineId,
        curPage,
        size
    }
    return get(`${baseUrl}/getOnedayMax`, params);
}
