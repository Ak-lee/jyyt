package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.YardShifts;
import com.example.yjyt.mapper.ShiftsMapper;
import com.example.yjyt.serv.ShiftsService;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author 29547
 * @description 针对表【shifts(班制表)】的数据库操作Service实现
 * @createDate 2022-10-31 11:19:25
 */
@Service
public class ShiftsServiceImpl extends ServiceImpl<ShiftsMapper, YardShifts>
        implements ShiftsService {
    public List<YardShifts> selectAll() {
        return baseMapper.selectList(null);
    }
}




