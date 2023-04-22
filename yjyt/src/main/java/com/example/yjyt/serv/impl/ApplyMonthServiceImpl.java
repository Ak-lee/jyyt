package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.ApplyMonth;
import com.example.yjyt.domain.ApplyMonthVO;
import com.example.yjyt.mapper.applyMonthMapper;
import com.example.yjyt.serv.ApplyMonthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author 29547
 * @description 针对表【tasktype_mode_apply_month】的数据库操作Service实现
 * @createDate 2022-11-21 17:00:18
 */
@Service
public class ApplyMonthServiceImpl extends ServiceImpl<applyMonthMapper, ApplyMonth>
        implements ApplyMonthService {

    @Autowired
    private TypeInfoServImpl tiServ;

    public List<ApplyMonthVO> table(Long tasktypeId) {
        // 根据检修任务类型 id
        // 首先获取所有的检修任务，组成一个列表。
        // 这个列表中的每个条目，又去查适用月份表
//        TaskTypeListVO result = tiServ.getListVOByTaskTypeId(tasktypeId);
//        List<Long> ids = new ArrayList<>();
//        result.getList().forEach(i -> {
//            ids.add(i.getId());
//        });
//
//        QueryWrapper<ApplyMonth> wrapper = new QueryWrapper<>();
//        wrapper.in("tasktype_mode_id", ids);
//        List<ApplyMonth> list = this.list(wrapper);
//
//        list.forEach(j -> {
//
//        })
        return baseMapper.getDetail(tasktypeId);
    }
}




