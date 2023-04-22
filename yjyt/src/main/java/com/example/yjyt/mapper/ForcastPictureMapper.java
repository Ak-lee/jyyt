package com.example.yjyt.mapper;

import com.example.yjyt.domain.ForcastPicture;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Select;

/**
 * @author 29547
 * @description 针对表【forcast_picture】的数据库操作Mapper
 * @createDate 2023-03-24 09:36:35
 * @Entity com.example.yjyt.domain.ForcastPicture
 */
public interface ForcastPictureMapper extends BaseMapper<ForcastPicture> {
    @Select("select picture from forcast_picture where train_id = #{trainId}")
    String getPictureByTrainId(String trainId);
}
