package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * @TableName tasktype_detail
 */
@TableName(value ="tasktype_detail")
@Data
public class TasktypeDetail implements Serializable {
    private Long id;

    private Long taskTypeId;

    private Integer requireHour;

    private Integer requireDay;

    private Integer requireHeadcount;

    private static final long serialVersionUID = 1L;
}