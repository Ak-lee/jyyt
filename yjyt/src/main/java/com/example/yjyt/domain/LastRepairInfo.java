package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("last_repair_info")
public class LastRepairInfo {
    private Integer id;
    private String trainId;
    private Integer lineId;
    private String mileageCheck;
    private String topCheck;
    private String balancedRepairDate;
    private String balancedRepair;
}
