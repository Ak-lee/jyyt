import {get, post, del, put} from '@/utils/request'

const baseUrl = '/api/planFeedback';


export const saveBatch = function(body) {
    return post(`${baseUrl}/batch`, body)
}
