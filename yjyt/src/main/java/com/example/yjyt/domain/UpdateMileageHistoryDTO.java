package com.example.yjyt.domain;

import com.alibaba.excel.annotation.format.DateTimeFormat;
import lombok.*;

import java.sql.Date;

@Data
public class UpdateMileageHistoryDTO {
    private MileageHistory mileageHistory;
    @DateTimeFormat("yyyy-MM-dd")
    private Date date;
    private String trainId;
}
