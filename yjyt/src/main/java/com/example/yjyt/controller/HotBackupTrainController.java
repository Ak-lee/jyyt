package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.toolkit.IdWorker;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.HotBackupTrainNum;
import com.example.yjyt.domain.ScheduleDay;
import com.example.yjyt.serv.impl.HotBackupTrainNumServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/hotBackupTrain")
public class HotBackupTrainController {

    @Autowired
    private HotBackupTrainNumServiceImpl serv;

    @GetMapping("/getItem")
    public R getByLineIdAndApplicable(
            @RequestParam("lineId") Integer lineId,
            @RequestParam("applicableTime") String applicableTime
    ) {
        List<HotBackupTrainNum> list = serv.getByLineIdAndApplicable(lineId, applicableTime);
        return R.ok().put("data", list);
    }

    @PostMapping("/addOrUpdate")
    public R addOrUpdateItem(@RequestBody HotBackupTrainNum item) {
        System.out.println(item);
        if (item.getId() != 0) {
            // 更新
            serv.updateById(item);
        } else {
            serv.save(item);
        }
        return R.ok();
    }

    @PostMapping("/list")
    public R saveList(@RequestBody List<HotBackupTrainNum> list) {
        List<HotBackupTrainNum> insertData = list.stream().filter(i -> i.getId() == null).collect(Collectors.toList());
        List<HotBackupTrainNum> updateData = list.stream().filter(i -> i.getId() != null).collect(Collectors.toList());

        insertData.forEach(i -> {
            i.setId(IdWorker.getId());
        });
        serv.saveBatch(insertData);
        if (!updateData.isEmpty()) {
            serv.updateBatchById(updateData);
        }
        return R.ok();
    }
}
