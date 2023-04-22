package com.example.yjyt.mapper;

import com.example.yjyt.domain.YardTaskTypeDetail;
import com.example.yjyt.domain.YardTasktype;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
* @author 29547
* @description 针对表【yard_tasktype_mapper】的数据库操作Mapper
* @createDate 2023-03-22 18:53:12
* @Entity com.example.yjyt.domain.YardTasktypeMapper
*/
public interface YardTasktypeMapper extends BaseMapper<YardTasktype> {
    @Select("select DISTINCT tasktype_id from yard_tasktype_mapper where yard_id = #{yardId}")
    public List<Long> getTaskTypesByYardId(String yardId);

    @Select("SELECT " +
            "td.*, "+
            " yt.*, " +
            " t.task_type_name, " +
            " t.be_multi_mode, " +
            " y.`name` yard_name " +
            "FROM " +
            " yard_tasktype_mapper yt " +
            " LEFT JOIN tasktype_info t ON yt.tasktype_id = t.id " +
            "LEFT JOIN tasktype_detail td  ON td.task_type_id = t.id "+
            " LEFT JOIN yard_info y ON yt.yard_id = y.id " +
            "WHERE " +
            " yard_id = #{yardId} and tasktype_id = #{tasktypeId} ")
    public List<YardTaskTypeDetail> getItemsByYardIdAndTasktypeId(String yardId, Long tasktypeId);
}




