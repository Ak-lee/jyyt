import {del, get, post, put} from '@/utils/request'


const baseUrl = '/api/workcalendar';

export const getCategoryInfoByCalendarId = function (calendarId) {
    let params = {
        calendarId,
    }
    return get(`${baseUrl}/getCategoryInfoByCalendarId`, params)
}

export const tableWithCond = function (calendarId, year, month) {
    let params = {
        calendarId,
        year,
        month
    }
    return get(`${baseUrl}/tableWithCond`, params)
}

export const update = function (body) {
    return put(`${baseUrl}`, body);
}


