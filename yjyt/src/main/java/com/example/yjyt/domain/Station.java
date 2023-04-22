package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.util.Date;

@Data
@TableName("station_info")
public class Station {
    @TableId(type = IdType.ASSIGN_ID)
    private Integer id;
    private String name;
    private Integer lineId;
    private String longitude;
    private String latitude;
    private String nearYard;
    private String belongto;

}
