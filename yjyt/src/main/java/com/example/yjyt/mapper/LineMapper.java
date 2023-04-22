package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.domain.LineInfo;
import com.example.yjyt.domain.LineInfoVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

@Repository
public interface LineMapper extends BaseMapper<LineInfo> {

    @Select({
            "<script> ",
            "select *, (select count(id) from train_info ",
            "where train_info.line_id = line_info.id) train_num ",
            "from line_info",
            "<if test='key != null'>",
            "where name like #{key}",
            "</if>",
            "</script> "
    })
    Page<LineInfoVO> getPage(Page<LineInfoVO> page, @Param("key") String key);

    @Select({
            "<script> ",
            "select *, (select count(id) from train_info ",
            "where train_info.line_id = line_info.id) train_num ",
            "from line_info",
            "where line_info.id =  #{lineId}",
            "</script> "
    })
    LineInfoVO getByLineId(Integer lineId);
}
