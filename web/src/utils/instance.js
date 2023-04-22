/**
 * 生成基础axios对象，并对请求和响应做处理
 * 前后端约定接口返回解构规范
 * {
 *    code:0,
 *    data:"成功",
 *    message:""
 * }
 */
 import axios from 'axios'
 import { ElMessage } from 'element-plus'
 
 // 创建一个独立的axios实例
 const jyyt_instance = axios.create({
     // 设置baseUr地址,如果通过proxy跨域可直接填写base地址
     baseURL: '/',
     // 定义统一的请求头部
     headers: {
         "Content-Type": "application/json;charset=UTF-8"
     },
     // 配置请求超时时间
     timeout: 30000,
 });
 // 请求拦截
 jyyt_instance.interceptors.request.use(config => {
     // 自定义header，可添加项目token
     config.headers.token = 'token';
     return config;
 });
 
 // 返回拦截
 jyyt_instance.interceptors.response.use((response) => {
     // 获取接口返回结果
     const res = response.data;
 
     return res;
 
 }, () => {
     ElMessage.error('网络请求异常，请稍后重试!');
 });
 
 export default jyyt_instance;
 