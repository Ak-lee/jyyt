import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/schedule_day';

export const table = function (scheduleId) {
    let params = {
        scheduleId
    }
    return get(`${baseUrl}/table`, params)
}

export const getById = function (id) {
    return get(`${baseUrl}/info/${id}`)
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
