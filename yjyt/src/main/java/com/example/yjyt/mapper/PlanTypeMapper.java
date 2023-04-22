package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.domain.PlanTypeInfo;
import com.example.yjyt.domain.PlanTypeInfoVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

@Repository
public interface PlanTypeMapper extends BaseMapper<PlanTypeInfo> {
    @Select("SELECT pt.id, pt.name, l.name as line_name, tt.task_type_name as task_type_name\n" +
            "FROM plan_type_mapper pt\n" +
            "LEFT JOIN line_info l on pt.line_id = l.id\n" +
            "LEFT JOIN tasktype_info tt on pt.tasktype_id = tt.id\n" +
            "WHERE pt.line_id = #{lineId}")
    public Page<PlanTypeInfoVO> getPage(Page<PlanTypeInfoVO> page, @Param("lineId") Integer lineId);

    @Select("SELECT pt.id, pt.name, l.name as line_name, tt.task_type_name as task_type_name\n" +
            "FROM plan_type_mapper pt\n" +
            "LEFT JOIN line_info l on pt.line_id = l.id\n" +
            "LEFT JOIN tasktype_info tt on pt.tasktype_id = tt.id\n")
    public Page<PlanTypeInfoVO> getPageAll(Page<PlanTypeInfoVO> page);

//    @Select("SELECT pt.id, pt.name, l.name as line_name, tt.task_type_name as task_type_name\n" +
//            "FROM plan_type_mapper pt\n" +
//            "LEFT JOIN line_info l on pt.line_id = l.id\n" +
//            "LEFT JOIN tasktype_info tt on pt.tasktype_id = tt.id\n" +
//            "WHERE pt.id = #{id}")
//    public PlanTypeInfoVO getOneById(String id);
}
