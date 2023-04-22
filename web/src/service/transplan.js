import {get, post, del, put} from '@/utils/request'


const baseUrl = '/api/transplan';

//这里将Pagesize改成了size,,pagenum变成curPage
export const table = function (curPage,size ,key) {
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

export const add = function (body) {

    return post(`${baseUrl}`, body);
}


export const update = function (body) {
    return put(`${baseUrl}`, body);
}

export const removeById = function (id) {

    return del(`${baseUrl}/info/${id}`)
}

export const getTransPlan = function (lineId ,applicableTime,curPage,size ,key) {
    let params = {
        lineId,
        applicableTime,
        curPage,
        size
    }
    if (key != null) {
        params.key = key;
    }
    return get(`${baseUrl}/getTransPlan`, params);
}

export const getTransPlan2 = function (lineId ,applicableTime) {
    let params = {
        lineId,
        applicableTime,
    }
    return get(`${baseUrl}/getTransPlan2`, params);
}