package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@EqualsAndHashCode
@ToString
@TableName("line_yard_mapper")
public class LineYardInfo {
    private Integer lineId;
    private String yardId;
}
