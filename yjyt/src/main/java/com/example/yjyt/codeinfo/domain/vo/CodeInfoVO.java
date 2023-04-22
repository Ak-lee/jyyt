package com.example.yjyt.codeinfo.domain.vo;

import com.example.yjyt.codeinfo.domain.CodeInfo;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Setter
@Getter
public class CodeInfoVO extends CodeInfo {
    private String id;
    private String name;
    private String expression;
    private List<Segment> segs;
    private String previewText;
    private String className;
}
