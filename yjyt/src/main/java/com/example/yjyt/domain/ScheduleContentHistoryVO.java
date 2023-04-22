package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;
import java.util.Date;

/**
 * @TableName schedule_content_history
 */
@TableName(value ="schedule_content_history")
@Data
public class ScheduleContentHistoryVO extends ScheduleContentHistory implements Serializable {
    private String planType;
}