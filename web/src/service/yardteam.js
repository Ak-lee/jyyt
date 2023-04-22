import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/yardteam';


export const table = function (yardId) {
    let params = {
        yardId,
    }
    return get(`${baseUrl}/table`, params)
}

export const add = function (body) {
    return post(`${baseUrl}`, body);
}

export const remove = function (body) {
    return del(`${baseUrl}`, body);
}

export const update = function (body) {
    return put(`${baseUrl}/`, body);
}