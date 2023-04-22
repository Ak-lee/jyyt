package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.ForcastMileage;
import com.example.yjyt.serv.ForcastMileageService;
import com.example.yjyt.mapper.ForcastMileageMapper;
import org.springframework.stereotype.Service;

import java.sql.Date;
import java.util.List;

/**
 * @author 29547
 * @description 针对表【forcast_mileage】的数据库操作Service实现
 * @createDate 2022-11-29 18:44:13
 */
@Service
public class ForcastMileageServiceImpl extends ServiceImpl<ForcastMileageMapper, ForcastMileage>
        implements ForcastMileageService {
    public ForcastMileage getItemByTrainIdAndDate(String trainId, Date date) {
        QueryWrapper<ForcastMileage> wrapper = new QueryWrapper<>();
        wrapper.eq("train_id", trainId).eq("calendar", date);
        ForcastMileage result = baseMapper.selectOne(wrapper);
        return result;
    }

    public List<ForcastMileage> getByTrainIdAndRange(String trainId, Date sdate, Date edate) {
        QueryWrapper<ForcastMileage> wrapper = new QueryWrapper<>();
        wrapper.eq("train_id", trainId).between("calendar", sdate, edate);
        List<ForcastMileage> list = baseMapper.selectList(wrapper);
        return list;
    }
}




