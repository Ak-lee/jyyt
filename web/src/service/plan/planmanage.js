import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/schedule';

export const table = function (key, curPage, size, planType) {
    let params = {
        key,
        curPage,
        size,
        planType
    }
    return get(`${baseUrl}/tabledata`, params)
}

export const tableAll = function (curPage, size, planType) {
    let params = {
        curPage,
        size,
        planType
    }
    return get(`${baseUrl}/tabledataall`, params);
}

export const tableDataAllNoPage = function(planType) {
    let params = {
        planType
    }
    return get(`${baseUrl}/tableDataAllNoPage`, params);
}

export const getById = function (id) {
    return get(`${baseUrl}/infoone/${id}`)
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
