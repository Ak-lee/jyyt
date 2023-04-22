package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.domain.TrainInfo;
import com.example.yjyt.domain.TrainInfoVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TrainMapper extends BaseMapper<TrainInfo> {
    @Select("select train_info.*, line_info.name as lineName from train_info \n" +
            "left join line_info on train_info.line_id = line_info.id \n" +
            "where train_info.line_id=#{lineId}")
    Page<TrainInfoVO> getPage(Page<TrainInfoVO> page, @Param("lineId") Integer lineId);

    @Select("select train_info.*, line_info.name as lineName from train_info \n" +
            "left join line_info on train_info.line_id = line_info.id \n" +
            "where train_info.line_id=#{lineId}")
    List<TrainInfoVO> getListByLineId(@Param("lineId") Integer lineId);

    @Select("select train_info.*, line_info.name as lineName from train_info \n " +
            "left join line_info on train_info.line_id = line_info.id")
    Page<TrainInfoVO> getPageAll(Page<TrainInfoVO> page);
}
