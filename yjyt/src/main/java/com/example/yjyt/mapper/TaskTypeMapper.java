package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.domain.*;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TaskTypeMapper extends BaseMapper<TaskTypeInfo> {
    @Select("select * from tasktype_info")
    public Page<TaskTypeInfoVO> getPageMain(Page<TaskTypeInfoVO> page);

    @Select("select DISTINCT task_type_id from tasktype_detail")
    public List<Long> getAllTaskTypes();

    @Select("SELECT " +
            "td.*, " +
            "t.task_type_name, " +
            "t.be_multi_mode " +
            "FROM " +
            "tasktype_detail td " +
            "LEFT JOIN tasktype_info t ON td.task_type_id = t.id " +
            "WHERE " +
            "task_type_id = #{tasktypeId}")
    public List<TaskTypeDetailVO> getItemsByTasktypeId(Long tasktypeId);
}
