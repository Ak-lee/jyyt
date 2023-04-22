package com.example.yjyt.domain;

import lombok.Data;

@Data
public class WorkCalendarCategoryByMonth {
    private Integer year;
    private Integer month;
    private Integer workDays;
    private Integer restDays;
    private String productionCalendarId;
}
