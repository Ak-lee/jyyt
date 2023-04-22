package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.ScheduleDay;
import com.example.yjyt.domain.ScheduleDayVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface ScheduleDayMapper extends BaseMapper<ScheduleDay> {
    @Select("SELECT\n" +
            "\tsd.*,\n" +
            "\tschedule_info.line_id,\n" +
            "\tschedule_content.plan_date,\n" +
            "\tschedule_content.duration\n" +
            "FROM\n" +
            "\tschedule_day sd\n" +
            "\tLEFT JOIN schedule_info ON schedule_info.id = sd.schedule_id\n" +
            "\tLEFT JOIN schedule_content ON sd.task_id = schedule_content.id \n" +
            "WHERE\n" +
            "\tsd.schedule_id = #{scheduleId}")
    public List<ScheduleDayVO> getContent(@Param("scheduleId") String scheduleId);
}
