package com.example.yjyt.domain;

import lombok.Data;

import java.util.List;

@Data
public class YardTaskTypeListVO {
    private String yardId;
    private String yardName;

    private Long taskTypeId;
    private String taskTypeName;

    private List<YardTaskTypeDetail> list;
}
