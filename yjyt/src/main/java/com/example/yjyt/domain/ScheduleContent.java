package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import org.springframework.format.annotation.DateTimeFormat;

import java.sql.Date;

@Data
@TableName("schedule_content")
public class ScheduleContent {
    String id;
    String scheduleId;
    String trainId;
    Integer lineId; // 返回对象时使用，上传时可能不使用该属性
    @JsonFormat(pattern = "yyyy-MM-dd", timezone = "GMT+8")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    Date planDate;
    Integer duration;
    String taskType;
    String taskContent;
    Integer applyMonth;
}

