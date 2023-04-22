package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableField;
import lombok.Data;

import java.sql.Date;

@Data
public class ScheduleDayVO extends ScheduleDay {
    public Integer lineId;
    @TableField(value = "plan_date")
    // 任务的执行时间，而非日计划的时间，特别是对于多日任务可能存在 task_date 与当前日计划的 date 不同
    public Date taskDate;
    public Integer duration;    // 计划的持续时间，
}
