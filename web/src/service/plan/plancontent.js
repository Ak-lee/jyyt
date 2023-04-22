import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/schedule_content';

export const table = function (scheduleId) {
    let params = {
        scheduleId
    }
    return get(`${baseUrl}/table`, params)
}

export const tableAll = function (lineId) {
    let params = {
        lineId
    }
    return get(`${baseUrl}/tableall`, params)
}

export const getLastTask = function (id) {
    return get(`${baseUrl}/getLastTask/${id}`)
}

export const getNextTask = function (id) {
    return get(`${baseUrl}/getNextTask/${id}`)
}

export const getNextTaskItem = function (planDate, taskType, trainId) {
    let params = {
        planDate,
        taskType,
        trainId
    }
    return get(`${baseUrl}/getNextTaskItem`, params);
}

export const getById = function (id) {
    return get(`${baseUrl}/info/${id}`)
}

export const addOrUpdate = function (body) {
    return post(`${baseUrl}/list`, body);
}


export const update = function (body) {
    return put(`${baseUrl}`, body);
}

export const removeById = function (id) {
    return del(`${baseUrl}/${id}/`)
}
