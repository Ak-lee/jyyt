package com.example.yjyt.domain;

import lombok.Data;

import java.util.List;

@Data
public class LineYardInfoDTO {
    private Integer lineId;
    private List<LineYardInfo> list;
}