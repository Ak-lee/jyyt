package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.YardTasktypeShift;
import com.example.yjyt.domain.YardTasktypeShiftVO;
import com.example.yjyt.serv.YardTasktypeShiftMapperService;
import com.example.yjyt.mapper.YardTasktypeShiftMapperMapper;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 29547
* @description 针对表【yard_tasktype_shift_mapper】的数据库操作Service实现
* @createDate 2022-11-26 14:53:33
*/
@Service
public class YardTasktypeShiftMapperServiceImpl extends ServiceImpl<YardTasktypeShiftMapperMapper, YardTasktypeShift>
    implements YardTasktypeShiftMapperService{

    public List<YardTasktypeShiftVO> tableByYardId(String yardId) {
        return baseMapper.tableByYardId(yardId);
    }

}




