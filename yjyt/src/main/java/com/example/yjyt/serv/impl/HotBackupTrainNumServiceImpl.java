package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.HotBackupTrainNum;
import com.example.yjyt.serv.HotBackupTrainNumService;
import com.example.yjyt.mapper.HotBackupTrainNumMapper;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 29547
* @description 针对表【hot_backup_train_num(热备份车辆数量)】的数据库操作Service实现
* @createDate 2023-03-24 23:03:34
*/
@Service
public class HotBackupTrainNumServiceImpl extends ServiceImpl<HotBackupTrainNumMapper, HotBackupTrainNum>
    implements HotBackupTrainNumService{
    public List<HotBackupTrainNum> getByLineIdAndApplicable(Integer lineId,
                                                            String applicableTime) {
        QueryWrapper<HotBackupTrainNum> wrapper = new QueryWrapper<>();
        wrapper.eq("line_id", lineId).eq("applicable_time", applicableTime);
        return baseMapper.selectList(wrapper);
    }
}




