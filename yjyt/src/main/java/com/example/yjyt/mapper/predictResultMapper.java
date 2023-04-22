package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.predResult;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface predictResultMapper extends BaseMapper<predResult> {
    @Select("select * from forcast_mileage")
    List<predResult> predResultPage();

    @Select("select train_id, MAX(date) date from jyyt.mileage_history GROUP BY train_id")
    List<predResult> getendTrainingList();
}