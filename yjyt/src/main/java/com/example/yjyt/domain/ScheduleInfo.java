
package com.example.yjyt.domain;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.*;

import java.sql.Date;

@Data
@TableName("schedule_info")
public class ScheduleInfo {
    @TableId(type = IdType.ASSIGN_ID)
    String id;
    Integer lineId;
    String name;
    String year;
    String planType;
    Date makeTime;
    Date startTime;
    Date endTime;
    String dispatchStatus;
    boolean feedbackStatus;
}

