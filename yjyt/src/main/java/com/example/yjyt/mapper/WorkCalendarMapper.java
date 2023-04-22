package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.TransPlanInfo;
import com.example.yjyt.domain.WorkCalendarCategoryByMonth;
import com.example.yjyt.domain.WorkCalendarInfo;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface WorkCalendarMapper extends BaseMapper<WorkCalendarInfo> {

    @Select("select year(date) year, month(date) month,\n" +
            "count(case when attribute=\"工作\" then 1 end) work_days,\n" +
            "count(case when attribute=\"休息\" then 1 end) rest_days,\n" +
            "production_calendar_id\n" +
            "from work_calendar\n" +
            "where production_calendar_id = #{productionCalendarId}\n" +
            " group by year(date), month(date)" +
            "")
    public List<WorkCalendarCategoryByMonth> categoryByMonth(String productionCalendarId);

    @Select("select * from work_calendar where production_calendar_id=#{calendarId} and year(date)=#{year} and month(date)=#{month} ")
    public List<WorkCalendarInfo> tableWithCond(String calendarId, Integer year, Integer month);
}
