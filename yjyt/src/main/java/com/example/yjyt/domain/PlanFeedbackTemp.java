package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;
import java.util.Date;

import lombok.Data;

/**
 * @TableName plan_feedback_temp
 */
@TableName(value = "plan_feedback_temp")
@Data
public class PlanFeedbackTemp implements Serializable {
    private Long id;

    private String scheduleId;

    private Integer lineId;

    private String trainId;

    private String taskType;

    private String taskContent;

    private Long taskId;

    private String taskSegment;

    private String taskSite;

    private String taskTeam;

    private Date date;

    private Integer duration;

    private Integer offsetDay;

    private String status;

    private Integer applyMonth;

    private static final long serialVersionUID = 1L;
}