package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.YardShifts;
import com.example.yjyt.domain.YardTasktypeShift;
import com.example.yjyt.domain.YardTasktypeShiftVO;
import com.example.yjyt.serv.impl.ShiftsServiceImpl;
import com.example.yjyt.serv.impl.YardTasktypeShiftMapperServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@RestController
@RequestMapping("/shifts")
public class YardTasktypeShiftController {
    @Autowired
    private YardTasktypeShiftMapperServiceImpl serv;

    @Autowired
    private ShiftsServiceImpl serv2;

    @GetMapping("/tableByYardIdAndTasktypeId")
    public R tableByYardIdAndTasktypeId(@RequestParam String yardId,
                                        @RequestParam String taskTypeId) {
        // 根据 yardId 和 taskTypeId 只能获取一个条目。
        QueryWrapper<YardTasktypeShift> wrapper = new QueryWrapper<>();
        wrapper.eq("yard_id", yardId);
        wrapper.eq("tasktype_id", taskTypeId);

        List<YardTasktypeShift> list = serv.list(wrapper);

        if (!list.isEmpty()) {
            YardTasktypeShift item = list.get(0);

            QueryWrapper<YardShifts> wrapper2 = new QueryWrapper<>();
            wrapper2.eq("id", item.getYardShiftsId());
            List<YardShifts> list2 = serv2.list(wrapper2);
            if (!list2.isEmpty()) {
                return R.ok().put("data", list2.get(0));
            } else {
                return R.error();
            }
        } else {
            return R.error();
        }
    }

    @GetMapping("/tableByYardId")
    public R tableByYardId(@RequestParam String yardId) {
        QueryWrapper<YardTasktypeShift> wrapper = new QueryWrapper<>();
        wrapper.eq("yard_id", yardId);
        List<YardTasktypeShiftVO> data = serv.tableByYardId(yardId);
        return R.ok().put("data", data);
    }

    @PostMapping
    public R save(@RequestBody YardTasktypeShift yardTasktypeShift) {
        serv.save(yardTasktypeShift);
        return R.ok();
    }

    @PutMapping
    public R update(@RequestBody YardTasktypeShift yardTasktypeShift) {
        QueryWrapper<YardTasktypeShift> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("id", yardTasktypeShift.getId());
        boolean result = serv.update(yardTasktypeShift, queryWrapper);
        if (result) {
            return R.saveOk(yardTasktypeShift);
        } else {
            return R.error();
        }
    }
}
