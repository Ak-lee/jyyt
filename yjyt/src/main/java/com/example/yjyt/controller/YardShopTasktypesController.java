package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.*;
import com.example.yjyt.serv.impl.YardShopTasktypesMapperServiceImpl;
import com.example.yjyt.serv.impl.YardTasktypeMapperServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/yardShopTasktypes")
public class YardShopTasktypesController {
    @Autowired
    private YardShopTasktypesMapperServiceImpl serv;

    @Autowired
    YardTasktypeMapperServiceImpl serv3;

    @GetMapping("/")
    public R getItem(@RequestParam(name = "yardId") String yardId,
                     @RequestParam(name = "tasktypeId") Long tasktypeId
    ) {
        QueryWrapper<YardShopTasktypes> wrapper = new QueryWrapper<>();
        wrapper.eq("yard_id", yardId);
        wrapper.eq("tasktype_id", tasktypeId);
        List<YardShopTasktypes> list = serv.list(wrapper);
        if (!list.isEmpty()) {
            return R.ok().put("data", list.get(0));
        } else {
            return R.ok().put("data", null);
        }
    }

    @GetMapping("/tableByYardId")
    public R tableByYardId(@RequestParam String yardId) {
        QueryWrapper<YardShopTasktypes> wrapper = new QueryWrapper<>();
        wrapper.eq("yard_id", yardId);
        List<YardShopTasktypes> data = serv.list(wrapper);
        return R.ok().put("data", data);
    }

    @PostMapping("/")
    public R saveItem(@RequestBody YardShopTasktypes item) {
        serv.saveItem(item);
        return R.ok();
    }

    @PutMapping("/")
    public R updateItem(@RequestBody YardShopTasktypes item) {
        QueryWrapper<YardShopTasktypes> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("id", item.getId());
        boolean result = serv.update(item, queryWrapper);
        if (result) {
            return R.saveOk(item);
        } else {
            return R.error();
        }
    }
}
