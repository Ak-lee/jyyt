package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.ForcastPicture;
import com.example.yjyt.serv.ForcastPictureService;
import com.example.yjyt.mapper.ForcastPictureMapper;
import org.springframework.stereotype.Service;

/**
* @author 29547
* @description 针对表【forcast_picture】的数据库操作Service实现
* @createDate 2023-03-24 09:36:35
*/
@Service
public class ForcastPictureServiceImpl extends ServiceImpl<ForcastPictureMapper, ForcastPicture>
    implements ForcastPictureService{
    public String getPredImg(String trainId) {
        return baseMapper.getPictureByTrainId(trainId);
    }
}




