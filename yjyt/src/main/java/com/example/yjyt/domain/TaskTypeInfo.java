package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.*;

import java.io.Serializable;

@Data
@TableName("tasktype_info")
public class TaskTypeInfo implements Serializable {
    private Long id;
    private String taskTypeName;
    private Integer mileagePeriod;
    private String timePeriod;          // 为方便季节专检的时间周期表示，这里使用字符串类型
    private boolean beAbsoluteTime;     // 是否为绝对时间，该字段为方便季节专检的时间周期表示。
    private boolean beMultiMode;        // 是否为多修程
    private Integer multiModeNum;       // 多修程中子修程的数量
}
