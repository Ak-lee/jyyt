package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.domain.LineInfo;
import com.example.yjyt.domain.Station;
import com.example.yjyt.domain.StationVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface StationMapper extends BaseMapper<Station> {
    //    @Select("select * from station_info s left join line_station_mapper m on s.id=m.station_id where m.line_id=#{lineId}")
//    @Select("select s.*, l.name as line_name from station_info s left join line_info l on s.line_id = l.id where line_id=#{lineId}")
    @Select("select s.*, l.name as line_name, y.name as near_yard_name " +
            "from station_info s \n" +
            "left join line_info l on s.line_id = l.id \n" +
            "left join yard_info y on s.near_yard = y.id\n" +
            "where s.line_id=#{lineId}")
    Page<StationVO> getPage(Page<StationVO> page, @Param("lineId") Integer lineId);

    @Select("select s.*, l.name as line_name, y.name as near_yard_name " +
            "from station_info s \n" +
            "left join line_info l on s.line_id = l.id \n" +
            "left join yard_info y on s.near_yard = y.id\n")
    Page<StationVO> getPageAll(Page<StationVO> page);
}
