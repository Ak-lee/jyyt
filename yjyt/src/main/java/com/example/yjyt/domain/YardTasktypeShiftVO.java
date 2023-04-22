package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;

/**
 * @TableName yard_tasktype_shift_mapper
 */
@TableName(value = "yard_tasktype_shift_mapper")
@Data
public class YardTasktypeShiftVO extends YardTasktypeShift implements Serializable {
    private String taskTypeName;
    private String shiftType;
}