
package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.domain.ScheduleInfo;
import com.example.yjyt.domain.ScheduleInfoVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.sql.Date;
import java.util.List;


@Repository
public interface ScheduleMapper extends BaseMapper<ScheduleInfo> {
    @Select("SELECT s.*, l.name as line_name\n" +
            "FROM schedule_info s\n" +
            "LEFT JOIN line_info l on s.line_id = l.id\n" +
            "WHERE s.plan_type = #{planType} and s.line_id = #{lineId}")
    public Page<ScheduleInfoVO> getPage(Page<ScheduleInfoVO> page, @Param("planType") String planType, @Param("lineId") Integer lineId);

    @Select("SELECT s.*, l.name as line_name\n" +
            "FROM schedule_info s\n" +
            "LEFT JOIN line_info l on s.line_id = l.id\n" +
            "WHERE s.plan_type = #{planType}")
    public Page<ScheduleInfoVO> getPageAll(Page<ScheduleInfoVO> page, @Param("planType") String planType);

    @Select("SELECT s.*, l.name as line_name\n" +
            "FROM schedule_info s\n" +
            "LEFT JOIN line_info l on s.line_id = l.id\n" +
            "WHERE s.id = #{id}")
    public ScheduleInfoVO getByIdOne(@Param("id") String id);
}
