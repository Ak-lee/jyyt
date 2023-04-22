package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("yard_team_mapper")
public class YardTeamInfo {
    private String yardId;
    private Integer teamId;
    private Integer num;
}
