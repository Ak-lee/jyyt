package com.example.yjyt.domain;

import lombok.Data;

import java.sql.Date;

@Data
public class ScheduleContentHistoryBeforeSync {
    // 存储同步之前的信息, 需要经过转换后，再以 ScheduleContentHistory 的格式存入数据库中.

    // 表示检修类型 这个需要详细的处理
    // 从中提取出检修任务类型、年份、月份等信息
    private String overhaulPlanName;
    private String overhaulTrainName;   // 车号信息
    private Date planStartDate; // 检修的开始时间
    private Date planEndDate;   // 检修的结束时间
}
