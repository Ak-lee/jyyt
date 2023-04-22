package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.Wrapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.Station;
import com.example.yjyt.domain.StationVO;
import com.example.yjyt.serv.impl.StationServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RequestMapping("/station")
@RestController
public class StationController {

    @Autowired
    private StationServImpl serv;

    @GetMapping("/table")
    public R tableAll(@RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                      @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<StationVO> page = new Page<>(curPage, size);
        serv.getPage(page);
        return R.ok().put("data", page);
    }

    @GetMapping("/table/{lineId}")  // get stations by lineId
    public R table(@PathVariable Integer lineId,
                   @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<StationVO> page = new Page<>(curPage, size);
        serv.getPageByLineId(page, lineId);
        return R.ok().put("data", page);
    }

    @PostMapping("/")
    public R saveItem(@RequestBody Station station) {
        Boolean result = serv.save(station);
        return R.ok().put("result", result);
    }

    @PutMapping("/")
    public R updateItem(@RequestBody Station station) {
        QueryWrapper<Station> queryWarpper = new QueryWrapper<>();
        queryWarpper.eq("id", station.getId());
        Boolean result = serv.update(station, queryWarpper);
        if (result) {
            return R.saveOk(station);
        } else {
            return R.error();
        }
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
