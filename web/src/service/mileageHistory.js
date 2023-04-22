import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/mileage_history';

export const getItemByTrainIdAndDate = function (trainId, date) {
    let params = {
        trainId,
        date
    }

    return get(`${baseUrl}/getByTrainIdAndDate`, params);
}

export const table = function () {
    return get(`${baseUrl}/table`);
}