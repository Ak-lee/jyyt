package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.sql.Date;

@Data
public class TrainInfo {
    private String id;
    private Integer lineId;
    private Date serviceStartDate;    // 使用 java.sql.Date
    private String trainStatus;
}
