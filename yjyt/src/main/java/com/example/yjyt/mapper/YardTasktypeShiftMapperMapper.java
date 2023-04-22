package com.example.yjyt.mapper;

import com.example.yjyt.domain.YardTasktypeShift;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.YardTasktypeShiftVO;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
* @author 29547
* @description 针对表【yard_tasktype_shift_mapper】的数据库操作Mapper
* @createDate 2022-11-26 14:53:33
* @Entity generator.domain.com.example.yjyt.domain.YardTasktypeShiftMapper
*/
public interface YardTasktypeShiftMapperMapper extends BaseMapper<YardTasktypeShift> {
    @Select("select yard_tasktype_shift_mapper.* ,\n" +
            "tasktype_info.task_type_name,\n" +
            "yard_shifts_mapper.type shiftType\n" +
            "from \n" +
            "yard_tasktype_shift_mapper\n" +
            "left join tasktype_info\n" +
            "on tasktype_id = tasktype_info.id\n" +
            "left join yard_shifts_mapper\n" +
            "on yard_shifts_id =  yard_shifts_mapper.id\n" +
            "where yard_tasktype_shift_mapper.yard_id = #{yardId}")
    public List<YardTasktypeShiftVO> tableByYardId(String yardId);
}




