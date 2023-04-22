import {get, post, del, put} from '@/utils/request'


const baseUrl = '/api/schedule';


export const table = function (curPage, size,key,id,name,year,planType,date1,date2) {
    let params = {
        curPage,
        size
    }
    if (key != null) {
        params.key = key;
    }
    if (id != null) {
        params.id = id;
    }
    if (name != null) {
        params.name = name;
    }
    if (year != null) {
        params.year = year;
    }
    if (planType != null) {
        params.planType = planType;
    }
    if (date1 != null) {
        params.date1 = date1;
    }
    if (date2 != null) {
        params.date2 = date2;
    }
    return get(`${baseUrl}/table`, params);
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

export const dispatchByIds = function(ids) {
    return put(`${baseUrl}/dispathByIds`, ids)
}