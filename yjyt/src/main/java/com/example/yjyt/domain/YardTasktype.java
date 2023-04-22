package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;

import lombok.Data;

/**
 * @TableName yard_tasktype_mapper
 */
@TableName(value = "yard_tasktype_mapper")
@Data
public class YardTasktype implements Serializable {
    String yardId;

    Long tasktypeId;

    static final long serialVersionUID = 1L;
}