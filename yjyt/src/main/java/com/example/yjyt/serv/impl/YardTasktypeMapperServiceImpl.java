package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.YardTaskTypeDetail;
import com.example.yjyt.domain.YardTaskTypeListVO;
import com.example.yjyt.domain.YardTasktype;
import com.example.yjyt.mapper.YardTasktypeMapper;
import com.example.yjyt.serv.YardTasktypeMapperService;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
* @author 29547
* @description 针对表【yard_tasktype_mapper】的数据库操作Service实现
* @createDate 2023-03-22 18:53:12
*/
@Service
public class YardTasktypeMapperServiceImpl extends ServiceImpl<YardTasktypeMapper, YardTasktype>
    implements YardTasktypeMapperService{
    public List<YardTaskTypeDetail> getListByYardIdAndTaskTypeId(String yardId, Long taskTypeId) {
        return baseMapper.getItemsByYardIdAndTasktypeId(yardId, taskTypeId);
    }

    public YardTaskTypeListVO getListVOByYardIdAndTaskTypeId(String yardId, Long taskTypeId) {
        // 将指定车场和任务类型的模式信息返回，信息中拼上了车场名称和任务类型名称
        List<YardTaskTypeDetail> list = getListByYardIdAndTaskTypeId(yardId, taskTypeId);

        if(list.isEmpty()) {
            return null;
        } else {
            YardTaskTypeListVO vo = new YardTaskTypeListVO();
            vo.setYardId(yardId);
            vo.setTaskTypeId(taskTypeId);
            vo.setTaskTypeName(list.get(0).getTaskTypeName());
            vo.setYardName(list.get(0).getYardName());
            vo.setList(list);
            return vo;
        }
    }

    public List<Long> getTaskTypesByYardId(String yardId) {
        return baseMapper.getTaskTypesByYardId(yardId);
    }

    public List<YardTaskTypeListVO> getByYardId(String yardId) {
        List<Long> taskTypeIds = getTaskTypesByYardId(yardId);
        List<YardTaskTypeListVO> list = new ArrayList<>();
        if (taskTypeIds.isEmpty()) {
            return null;
        }
        taskTypeIds.forEach(i -> {
            list.add(getListVOByYardIdAndTaskTypeId(yardId, i));
        });
        return list;
    }
}




