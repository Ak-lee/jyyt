package com.example.yjyt.controller;

import com.example.yjyt.common.R;
import com.example.yjyt.exception.BusinessException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.validation.BindException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * 统一异常处理、数据预处理等
 */
@ControllerAdvice
public class ControllerExceptionHandler {
    private static final Logger LOG = LoggerFactory.getLogger(ControllerExceptionHandler.class);

    /**
     * 校验异常统一处理
     */
    @ExceptionHandler(value = BindException.class)
    @ResponseBody
    public R validExceptionHandler(BindException e) {
        String msg = String.format("参数校验失败：%s", e.getBindingResult().getAllErrors().get(0).getDefaultMessage());
        LOG.warn(msg);
        return R.error(msg);
    }

    /**
     * 业务异常统一处理
     */
    @ExceptionHandler(value = BusinessException.class)
    @ResponseBody
    public R validExceptionHandler(BusinessException e) {
        String msg = String.format("业务异常：%s", e.getDesc());
        LOG.warn(msg);

        return R.error(msg);
    }

    /**
     * 系统异常统一处理
     */
    @ExceptionHandler(value = Exception.class)
    @ResponseBody
    public R validExceptionHandler(Exception e) {
        LOG.error("系统异常：", e);
        return R.error("系统出现异常，请联系管理员");
    }
}
