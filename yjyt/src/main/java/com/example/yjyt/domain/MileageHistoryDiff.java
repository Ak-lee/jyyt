package com.example.yjyt.domain;

import com.alibaba.excel.annotation.format.DateTimeFormat;
import lombok.*;

import java.sql.Date;

@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
public class MileageHistoryDiff {
    private String trainId;
    private int mileageDiff;
}
