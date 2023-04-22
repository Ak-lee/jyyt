package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;

/**
 * @TableName tasktype_mode_apply_month
 */
@TableName(value ="tasktype_mode_apply_month")
@Data
public class ApplyMonth implements Serializable {
    private String id;

    private Integer applyMonth;

    private String tasktypeModeId;

    private static final long serialVersionUID = 1L;
}