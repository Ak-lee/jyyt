import {get, post, put} from '@/utils/request'


const baseUrl = '/api/hotBackupTrain';


export const getItem = function (lineId,
                                 applicableTime) {
    let params = {lineId, applicableTime};
    return get(`${baseUrl}/getItem/`, params);
}

export const addOrUpdate = function (body) {
    return post(`${baseUrl}/addOrUpdate`, body);
}
