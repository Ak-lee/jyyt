package com.example.yjyt.codeinfo.domain.dto;

import com.example.yjyt.codeinfo.domain.vo.Segment;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Setter
@Getter
public class CodeDTO {
    private String id;
    private String name;
    private String expression;
    private List<Segment> segments;
    private Integer seq;
}
