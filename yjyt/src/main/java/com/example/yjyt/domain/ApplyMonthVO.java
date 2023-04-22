package com.example.yjyt.domain;

import lombok.Data;

@Data
public class ApplyMonthVO {
    private String id;
    private Integer applyMonth;
    private Long tasktypeModeId;
    private Integer requireDay;
    private Integer requireHeadcount;
    private Integer requireHour;
    private String taskTypeName;
}
