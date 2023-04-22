
package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.*;

@Data
@TableName("team_info")
public class TeamInfo {
    @TableId(type = IdType.ASSIGN_ID)
    Integer id;
    String teamType;
    Integer staffNum;
    String skills;
}

