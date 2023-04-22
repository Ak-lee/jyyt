import {del, get, post, put} from '@/utils/request'

const baseUrl = '/api/schedule_content_history';

export const table = function (scheduleId) {
    let params = {
        scheduleId
    }
    return get(`${baseUrl}/table`, params)
}

export const tableAll = function () {
    return get(`${baseUrl}/tableAll`)
}

export const getPagesOverview = function (lineId, planTypes) {
    let params = {
        lineId,
    }
    if (planTypes.length) {
        params.planTypes = planTypes.join(",")
    }
    return get(`${baseUrl}/getPagesOverview`, params)
}

export const tableWithCond = function (
    lineId,
    planTypes,
    sdate,
    edate,
    status
) {
    let params = {
        lineId,
    }
    if (planTypes && planTypes.length) {
        params.planTypes = planTypes.join(",")
    }
    if (sdate) {
        params.sdate = sdate;
    }
    if (edate) {
        params.edate = edate;
    }
    if (status) {
        params.status = status
    }
    return get(`${baseUrl}/tableWithCond`, params)
}

export const add = function (body) {
    return post(`${baseUrl}/`, body);
}

export const addBatch = function(body) {
    return post(`${baseUrl}/batch`, body);
}



export const update = function (body) {
    return put(`${baseUrl}/`, body);
}

export const removeById = function (id) {
    return del(`${baseUrl}/${id}/`)
}
