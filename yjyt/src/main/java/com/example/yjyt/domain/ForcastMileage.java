package com.example.yjyt.domain;

import com.alibaba.excel.annotation.format.DateTimeFormat;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;
import java.sql.Date;

/**
 * @TableName forcast_mileage
 */
@TableName(value = "forcast_mileage")
@Data
public class ForcastMileage implements Serializable {
    private String trainId;

    private Integer mileage;

    private Date calendar;

    private static final long serialVersionUID = 1L;
}

