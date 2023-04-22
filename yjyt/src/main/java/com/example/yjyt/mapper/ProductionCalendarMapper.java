package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.domain.ProductionCalendar;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.sql.Date;
import java.util.List;

/**
 * @author 29547
 * @description 针对表【production_calendar(生产日历信息)】的数据库操作Mapper
 * @createDate 2022-11-07 15:33:09
 * @Entity com.example.yjyt.domain.ProductionCalendar
 */
public interface ProductionCalendarMapper extends BaseMapper<ProductionCalendar> {
    @Select("select * from production_calendar where line_id=#{lineId}")
    Page<ProductionCalendar> getPage(Page<ProductionCalendar> page, @Param("lineId") Integer lineId);

    @Select("select * from production_calendar where line_id=#{lineId}")
    List<ProductionCalendar> getList(@Param("lineId") Integer lineId);

    @Select("select * from production_calendar where line_id=#{lineId} and  #{date} between start_date and end_date")
    ProductionCalendar getItem(Integer lineId, Date date);
}




