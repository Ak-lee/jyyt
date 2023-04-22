package com.example.yjyt.codeinfo.domain.vo;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * 编码字段,不同type规则如下：
 *    0 - 常量字符串，value 为字符串本身
 *    1 - 时间戳，value 为格式选择
 *    2 - 流水号，value 为位数，起始值，增量
 */
@AllArgsConstructor
@NoArgsConstructor
@Setter
@Getter
public class Segment {
    private String value;
    private Integer type;
    private Integer sort;
}
