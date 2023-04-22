package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.ApplyMonth;
import com.example.yjyt.domain.ApplyMonthVO;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
* @author 29547
* @description 针对表【tasktype_mode_apply_month】的数据库操作Mapper
* @createDate 2022-11-21 17:00:18
* @Entity com.example.yjyt.domain.applyMonth
*/
@Repository
public interface applyMonthMapper extends BaseMapper<ApplyMonth> {
    @Select("select tasktype_mode_apply_month.*, tasktype_detail.require_day, \n" +
            "tasktype_detail.require_hour,\n" +
            "tasktype_detail.require_headcount,\n" +
            "tasktype_info.task_type_name\n" +
            "from tasktype_mode_apply_month\n" +
            "left join tasktype_detail on tasktype_detail.id = tasktype_mode_id\n" +
            "left join tasktype_info on tasktype_info.id = tasktype_detail.task_type_id\n" +
            "where tasktype_info.id = #{tasktypeInfoId}\n")
    public List<ApplyMonthVO> getDetail(Long tasktypeInfoId);
}




