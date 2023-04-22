package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.*;
import com.example.yjyt.exception.BusinessException;
import com.example.yjyt.mapper.TaskTypeMapper;
import com.example.yjyt.serv.TypeInfoServ;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class TypeInfoServImpl extends ServiceImpl<TaskTypeMapper, TaskTypeInfo> implements TypeInfoServ {

    public boolean updateById(TaskTypeInfo taskTypeInfo) {
        return baseMapper.updateById(taskTypeInfo) > 0;
    }

    public boolean save(TaskTypeInfo taskTypeInfo) {
        TaskTypeInfo item = baseMapper.selectById(taskTypeInfo.getId());
        if (item == null) {
            baseMapper.insert(taskTypeInfo);
            return true;
        } else {
            throw new BusinessException("id 已存在");
        }
    }

    public List<TaskTypeInfo> getAll() {
        return baseMapper.selectList(null);
    }

    public TaskTypeListVO getListVOByTaskTypeId(Long taskTypeId) {
        // 将制定任务类型的模式信息返回，信息中拼上了任务类型名称

        List<TaskTypeDetailVO> list = baseMapper.getItemsByTasktypeId(taskTypeId);

        TaskTypeListVO vo = new TaskTypeListVO();
        vo.setTaskTypeId(taskTypeId);

        vo.setTaskTypeName(list.get(0).getTaskTypeName());
        vo.setList(list);

        return vo;
    }

    public List<Long> getAllTaskTypes() {
        return baseMapper.getAllTaskTypes();
    }

    public List<TaskTypeListVO> getWithTasktypeDetail() {
        // 首先获取所有的检修任务类型
        List<Long> taskTypeIds = baseMapper.getAllTaskTypes();
        List<TaskTypeListVO> list = new ArrayList<>();

        if (taskTypeIds.isEmpty()) {
            return null;
        }
        taskTypeIds.forEach(i -> {
            list.add(getListVOByTaskTypeId(i));
        });
        return list;
    }
}
