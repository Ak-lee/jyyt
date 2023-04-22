package com.example.yjyt.domain;

import lombok.Data;

@Data
public class TaskTypeDetailVO extends TasktypeDetail{
    private String taskTypeName;
    private boolean beMultiMode;
}
