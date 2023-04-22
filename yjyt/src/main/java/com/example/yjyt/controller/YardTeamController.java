package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.YardTeamInfo;
import com.example.yjyt.domain.YardTeamInfoDTO;
import com.example.yjyt.serv.impl.YardTeamInfoServImpl;
import com.example.yjyt.util.CopyUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RequestMapping("/yardteam")
@RestController
public class YardTeamController {

    @Autowired
    private YardTeamInfoServImpl serv;

    @GetMapping("/table")
    public R tableByYardId(@RequestParam(name = "yardId", required = true) String yardId) {
        return R.ok().put("data", serv.getByYardId(yardId));
    }

    @PostMapping
    public R save(@RequestBody YardTeamInfo item) {
        return R.ok().put("data", serv.save(item));
    }

    @DeleteMapping
    public R delete(@RequestBody YardTeamInfo item) {
        QueryWrapper<YardTeamInfo> wrapper = new QueryWrapper<>();
        wrapper.eq("yard_id", item.getYardId()).eq("team_id", item.getTeamId());
        serv.remove(wrapper);
        return R.ok();
    }

    @PutMapping
    public R update(@RequestBody YardTeamInfo item) {
        QueryWrapper<YardTeamInfo> wrapper = new QueryWrapper<>();
        wrapper.eq("yard_id", item.getYardId()).eq("team_id", item.getTeamId());
        serv.update(item, wrapper);
        return R.ok();
    }
}
