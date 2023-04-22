import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/applyMonth';

export const table = function (tasktypeId) {
    let params = {
        tasktypeId,
    }
    return get(`${baseUrl}/table`, params);
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
