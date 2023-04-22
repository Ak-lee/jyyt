package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;
import java.util.Date;

@Data
public class YardTaskTypeDetail extends YardTasktype{
    private String yardName;
    private String taskTypeName;

    private boolean beMultiMode;

    private Long id;

    private Long taskTypeId;

    private Integer requireHour;

    private Integer requireDay;

    private Integer requireHeadcount;
}
