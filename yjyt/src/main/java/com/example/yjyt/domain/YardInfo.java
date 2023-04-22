package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.*;

@Data
@TableName("yard_info")
public class YardInfo {
    private String id;
    private String name;
    private String longitude;
    private String latitude;
    private boolean beDepot;   // 是否为车辆段
    private boolean hasServiceShop;   // 是否有检修库
    private int serviceShopTrackwayNum;  // 检修库股道数量
    private boolean hasOperationShop;     // 是否有运用库
    private int operationShopTrackwayNum;    // 运用库股道数量
}
