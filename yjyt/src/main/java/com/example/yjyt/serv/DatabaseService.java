package com.example.yjyt.serv;

import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.example.yjyt.domain.*;
import com.example.yjyt.mapper.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.HashMap;
import java.util.Map;

@Service
public class DatabaseService {
    @Autowired
    private LineMapper lineMapper;
    @Autowired
    private TrainMapper trainMapper;
    @Autowired
    private TaskTypeMapper taskTypeMapper;
    @Autowired
    private YardMapper yardMapper;

    public List<LineInfo> getLineList() {
        return this.lineMapper.selectList(null);
    }

    public List<TrainInfo> getTrainList() {
        return this.trainMapper.selectList(null);
    }

    public List<TrainInfo> getTrainInfoList(int lineId) {
        Map<String, Object> map = new HashMap<>();
        map.put("line_id", lineId);
        return trainMapper.selectByMap(map);
    }

    public List<TaskTypeInfo> getTasktypeList() {
        return this.taskTypeMapper.selectList(null);
    }

    public List<YardInfo> getYardList() {
        return this.yardMapper.selectList(null);
    }

    public int postTasktypeList(TaskTypeInfo typeInfo) {
        UpdateWrapper<TaskTypeInfo> updateWrapper = new UpdateWrapper<>();
        updateWrapper.eq("tasktype_name", typeInfo.getTaskTypeName());
        return this.taskTypeMapper.update(typeInfo, updateWrapper);
    }
}