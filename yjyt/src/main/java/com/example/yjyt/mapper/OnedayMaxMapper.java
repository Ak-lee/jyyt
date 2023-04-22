package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.domain.OnedayMaxInfo;
import com.example.yjyt.domain.OnedayMaxInfoVO;
import com.example.yjyt.domain.ScheduleInfoVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

@Repository
public interface OnedayMaxMapper extends BaseMapper<OnedayMaxInfo> {
    @Select("SELECT s.*, l.name as line_name\n" +
            "FROM oneday_max s\n" +
            "LEFT JOIN line_info l on s.line_id = l.id\n" +
            "WHERE s.line_id = #{lineId}")
    public Page<OnedayMaxInfoVO> getPage(Page<OnedayMaxInfoVO> page, @Param("lineId") Integer lineId);

    @Select("SELECT s.*, l.name as line_name\n" +
            "FROM oneday_max s\n" +
            "LEFT JOIN line_info l on s.line_id = l.id")
    public Page<OnedayMaxInfoVO> getPageAll(Page<OnedayMaxInfoVO> page);
}
