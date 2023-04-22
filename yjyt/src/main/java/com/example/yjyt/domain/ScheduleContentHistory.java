package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.io.Serializable;
import java.util.Date;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import org.springframework.format.annotation.DateTimeFormat;

/**
 * @TableName schedule_content_history
 */
@TableName(value = "schedule_content_history")
@Data
public class ScheduleContentHistory implements Serializable {
    @TableId(type = IdType.ASSIGN_ID)
    private String id;

    private String scheduleId;

    private String trainId;

    private Integer lineId;

    private Integer applyMonth;

    @JsonFormat(pattern = "yyyy-MM-dd", timezone = "GMT+8")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date performDate;

    private Integer duration;

    private String taskType;

    private String taskContent;

    private String status;

    private String workYard;    // 检修车场的名字 name，而不是 ID

    private String taskSite;

    private String taskTeam;

    private Integer offsetDay;

    private static final long serialVersionUID = 1L;
}