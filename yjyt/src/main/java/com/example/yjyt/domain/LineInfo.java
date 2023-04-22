package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("line_info")
public class LineInfo {
    private Integer id;
    private String name;
    private Integer journeyTime;        // 单程运行时间
    private Double lineLength;
    private String remark;      // 备注
}
