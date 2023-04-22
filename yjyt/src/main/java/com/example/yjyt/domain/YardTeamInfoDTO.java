package com.example.yjyt.domain;

import lombok.Data;

import java.util.List;

@Data
public class YardTeamInfoDTO {
    private String yardId;
    private List<YardTeamInfo> list;
}