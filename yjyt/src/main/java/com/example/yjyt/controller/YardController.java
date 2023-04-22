package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.LineYardInfo;
import com.example.yjyt.domain.TeamInfo;
import com.example.yjyt.domain.YardInfo;
import com.example.yjyt.serv.LineYardInfoServ;
import com.example.yjyt.serv.impl.YardInfoServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RequestMapping("/yard")
@RestController
public class YardController {

    @Autowired
    private YardInfoServImpl serv;

    @Autowired
    private LineYardInfoServ lyserv;

    @GetMapping("/table")
    public R table(@RequestParam(name = "key", required = false) String key,
                   @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<YardInfo> page = new Page(curPage, size);
        serv.page(page, Wrappers.<YardInfo>lambdaQuery());
        return R.ok().put("data", page);
    }

    @GetMapping("/tableNoPage")
    public R tableNoPage() {
        List<YardInfo> data = serv.list(Wrappers.<YardInfo>lambdaQuery());
        return R.ok().put("data", data);
    }


    @GetMapping("/list")
    public R list(@RequestParam(name = "lineId", required = false) Integer lineId) {
        if (lineId != null) {
            QueryWrapper<LineYardInfo> qw = new QueryWrapper<>();
            qw.eq("line_id", lineId);
            List<LineYardInfo> list = lyserv.list(qw);
            List<String> yardIds = new ArrayList<>();
            for (LineYardInfo ly : list) {
                yardIds.add(ly.getYardId());
            }
            if (yardIds.isEmpty()) {
                return R.ok().put("data", null);
            }
            return R.ok().put("data", serv.listByIds(yardIds));
        } else {
            return R.ok().put("data", serv.getAllYards());
        }
    }

    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") String id) {
        YardInfo yardInfo = serv.getById(id);

        return R.ok().put("data", yardInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody YardInfo yardInfo) {
        serv.save(yardInfo);
        return R.ok();
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody YardInfo yardInfo) {
        serv.updateById(yardInfo);
        return R.ok();
    }


    /**
     * 删除
     */
    @DeleteMapping("/{id}")
    public R delete(@PathVariable String id) {
        serv.removeById(id);
        return R.ok();
    }
}
