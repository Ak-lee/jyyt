package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.sql.Time;

@Data
@TableName("schedule_day")
public class ScheduleDay {
    @TableId(type = IdType.ASSIGN_ID)
    Long id;
    String scheduleId;
    String trainId;
    Time startTime;
    Time endTime;
    String taskType;
    String taskContent;
    Integer applyMonth;
    String taskSegment;
    String taskSite;
    String taskTeam;
    String taskId;
    Integer offsetDay;  // 仅在任务为多日任务时有效，从0开始，方便用直接用加法
}