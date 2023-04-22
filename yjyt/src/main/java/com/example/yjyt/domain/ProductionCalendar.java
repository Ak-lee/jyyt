package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;
import java.util.Date;

import lombok.Data;
import org.springframework.format.annotation.DateTimeFormat;

/**
 * 生产日历信息
 *
 * @TableName production_calendar
 */
@TableName(value = "production_calendar")
@Data
public class ProductionCalendar implements Serializable {
    /**
     * 日历编号
     */
    @TableId
    private String id;

    /**
     * 所属线路ID
     */
    private Integer lineId;

    /**
     * 日历名称
     */
    private String name;

    /**
     * 开始日期
     */
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date startDate;

    /**
     * 结束日期
     */
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date endDate;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}
