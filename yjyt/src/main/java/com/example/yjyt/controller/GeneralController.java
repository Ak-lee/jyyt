package com.example.yjyt.controller;

import com.example.yjyt.domain.*;
import com.example.yjyt.mapper.TaskTypeMapper;
import com.example.yjyt.serv.DatabaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class GeneralController {
    @Autowired
    private DatabaseService databaseService;
    @Autowired
    private TaskTypeMapper taskTypeMapper;


    @GetMapping("/line_list")
    public List<LineInfo> getLineList() {
        return databaseService.getLineList();
    }

    @GetMapping("/train_list/{lineId}")
    public List<TrainInfo> getTrainList(@PathVariable("lineId") Integer lineId) {
        return databaseService.getTrainInfoList(lineId);
    }

    @GetMapping("/tasktype_list")
    public List<TaskTypeInfo> getTasktypeList() {
        return databaseService.getTasktypeList();
    }

    @GetMapping("/yard_list")
    public List<YardInfo> getYardList() {
        return databaseService.getYardList();
    }

    @RequestMapping(value = "/tasktype_update", method = RequestMethod.POST)
    public int postTasktypeList(@RequestBody TaskTypeInfo taskTypeInfo) {
        return databaseService.postTasktypeList(taskTypeInfo);
    }
}
