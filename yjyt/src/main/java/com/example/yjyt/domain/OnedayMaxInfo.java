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
@TableName("oneday_max")
public class OnedayMaxInfo {
   private Integer id;
   private Integer lineId;
   private Integer maxBalancedRepairs;
   private Integer maxMileageChecks;

}
