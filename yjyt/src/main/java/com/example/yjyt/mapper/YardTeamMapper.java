package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.YardTeamInfo;
import com.example.yjyt.domain.YardTeamInfoVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

public interface YardTeamMapper extends BaseMapper<YardTeamInfo> {
    @Select("select yard_team_mapper.*, yard_info.name yard_name, team_info.team_type team_type \n" +
            "from yard_team_mapper left join yard_info on yard_team_mapper.yard_id = yard_info.id\n" +
            "left join team_info on yard_team_mapper.team_id = team_info.id \n" +
            "where yard_id = #{yardId}"
    )
    List<YardTeamInfoVO> getVOByYardId(@Param("yardId") String yardId);
}
