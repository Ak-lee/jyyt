package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;
import java.sql.Time;
import java.util.Date;

import lombok.Data;

/**
 * 班制表
 *
 * @TableName shifts
 */
@TableName(value = "yard_shifts_mapper")
@Data
public class YardShifts implements Serializable {
    /**
     * 序号
     */
    @TableId
    private Integer id;

    /**
     * 班制编码
     */
    private String code;

    /**
     * 车场 ID
     */
    private String yardId;

    /**
     * 班制类型
     */
    private String type;

    /**
     * 开始时间（24小时制）
     */
    private Time beginTime;


    /**
     * 结束时间（24小时制）
     */
    private Time endTime;

    /**
     * 是否跨日（0 否， 1 是）
     */
    private Integer iscrossday;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}