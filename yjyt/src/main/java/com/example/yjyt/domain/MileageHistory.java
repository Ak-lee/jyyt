package com.example.yjyt.domain;

import com.alibaba.excel.annotation.format.DateTimeFormat;
import lombok.*;

import java.sql.Date;

@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
public class MileageHistory {
    private String trainId;
    private int mileage;
    @DateTimeFormat("yyyy-MM-dd")
    private Date date;    // 使用 java.sql.Date
}
