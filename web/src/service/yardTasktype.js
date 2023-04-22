import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/yardTasktype';


export const tableByYardId = function (yardId) {
    let params = {yardId};
    return get(`${baseUrl}/byYard`, params);
}

export const tableByYardIdAndTasktypeId = function (yardId, taskTypeId) {
    let params = {yardId, taskTypeId};
    return get(`${baseUrl}/byYardIdAndTasktypeId`, params);
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
