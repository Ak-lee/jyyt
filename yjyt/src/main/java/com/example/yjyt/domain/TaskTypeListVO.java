package com.example.yjyt.domain;

import lombok.Data;

import java.util.List;

@Data
public class TaskTypeListVO {
    private Long taskTypeId;
    private String taskTypeName;

    private List<TaskTypeDetailVO> list;
}