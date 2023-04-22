package com.example.yjyt.domain;

import lombok.Data;

import java.util.List;

@Data
public class YardTaskTypeDTO {
    private String yardId;
    private List<YardTasktype> list;
}