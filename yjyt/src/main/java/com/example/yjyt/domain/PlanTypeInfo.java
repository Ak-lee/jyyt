package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;

@Data
@TableName("plan_type_mapper")
public class PlanTypeInfo implements Serializable {
    private String id;
    private String name;
    private Integer lineId;
    private String tasktypeId;
}
