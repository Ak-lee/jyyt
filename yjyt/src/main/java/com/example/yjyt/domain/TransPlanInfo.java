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
@TableName("trans_manage")
public class TransPlanInfo {
    Integer id;
    Integer undercarId;
    Integer lineId;
    String outstorageSite;
    String instorageSite;
    String outyardTime;
    String inyardTime;
    String applicableTime;
}
