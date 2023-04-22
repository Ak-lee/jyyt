import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/dayPlanHistory';


export const table = function (lineId, date) {
    let params = {
        lineId,
        date
    }
    return get(`${baseUrl}/`, params)
}

export const clearAndAdd = function (body) {
    return post(`${baseUrl}/clearAndAdd`, body);
}
