package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * @TableName yard_tasktype_shift_mapper
 */
@TableName(value ="yard_tasktype_shift_mapper")
@Data
public class YardTasktypeShift implements Serializable {
    private Long id;
    private String yardId;
    private Long tasktypeId;
    private Integer yardShiftsId;
    private static final long serialVersionUID = 1L;
}