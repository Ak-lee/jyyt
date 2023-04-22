import {get, post, del, put} from '@/utils/request'


const baseUrl = '/api/team';


export const tableall = function () {
    let params = null;
    return get(`${baseUrl}/tableall`, params);
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

    return del(`${baseUrl}/${id}`)
}
