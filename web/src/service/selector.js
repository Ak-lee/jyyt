import {get} from '@/utils/request'

export const selectLine = function () {
    return get("/api/line_list");
};

export const selectYard = function () {
    return get("/api/yard_list");
};

export const selectTasktype = function () {
    return get("/api/tasktype_list");
};

export const selectTrain = function (lineId) {
    return get(`/api/train_list/${lineId}`)
}