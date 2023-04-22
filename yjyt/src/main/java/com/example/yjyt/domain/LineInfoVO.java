package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("line_info")
public class LineInfoVO extends LineInfo {
    private Integer id;
    private String name;
    private Integer trainNum;
    private Integer journeyTime;
    private Double lineLength;
    private String remark;
}
