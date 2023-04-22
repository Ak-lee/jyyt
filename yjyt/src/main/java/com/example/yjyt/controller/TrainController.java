package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.TrainInfo;
import com.example.yjyt.domain.TrainInfoVO;
import com.example.yjyt.serv.impl.TrainInfoServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/train")
@RestController
public class TrainController {
    @Autowired
    private TrainInfoServImpl serv;

    @GetMapping("/table")
    public R tableAll(@RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                      @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<TrainInfoVO> page = new Page<>(curPage, size);
        serv.getPage(page);
        return R.ok().put("data", page);
    }

    @GetMapping("/table/{lineId}")  // get stations by lineId
    public R table(@PathVariable Integer lineId,
                   @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<TrainInfoVO> page = new Page<>(curPage, size);
        serv.getPageByLineId(page, lineId);
        return R.ok().put("data", page);
    }

    @GetMapping("/tableNoPage/{lineId}")
    public R table(@PathVariable Integer lineId) {
        List<TrainInfoVO> list = serv.getByLineId(lineId);
        return R.ok().put("data", list);
    }

    @PostMapping("/")
    public R saveItem(@RequestBody TrainInfo train) {
        Boolean result = serv.save(train);
        return R.ok().put("result", result);
    }

    @PutMapping("/")
    public R updateItem(@RequestBody TrainInfo train) {
        QueryWrapper<TrainInfo> queryWarpper = new QueryWrapper<>();
        queryWarpper.eq("id", train.getId());
        Boolean result = serv.update(train, queryWarpper);
        if (result) {
            return R.saveOk(train);
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
