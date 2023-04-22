package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.StringUtils;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.OnedayMaxInfo;
import com.example.yjyt.domain.OnedayMaxInfoVO;
import com.example.yjyt.domain.ScheduleInfo;
import com.example.yjyt.domain.ScheduleInfoVO;
import com.example.yjyt.serv.impl.OnedayMaxServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/onedayMax")
@RestController
public class OnedayMaxController {

    @Autowired
    private OnedayMaxServImpl serv;

    @GetMapping("/table")
    public R table(@RequestParam(name = "lineId") Integer lineId,
                   @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<OnedayMaxInfoVO> page = new Page(curPage, size);
        serv.getPageByLineId(page, lineId);
        return R.ok().put("data", page);
    }

    @GetMapping("/tableAll")
    public R table(@RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<OnedayMaxInfoVO> page = new Page(curPage, size);
        serv.getPage(page);
        return R.ok().put("data", page);
    }

    @GetMapping("/tableAllByLineId")
    public R tableAllByLineId(@RequestParam(name = "lineId") Integer lineId) {
        List<OnedayMaxInfo> data = serv.getAllByLineId(lineId);
        return R.ok().put("data", data);
    }

    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") String id) {
        OnedayMaxInfo OnedayMaxInfo = serv.getById(id);

        return R.ok().put("data", OnedayMaxInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody OnedayMaxInfo onedayMaxInfo) {
        serv.save(onedayMaxInfo);
        return R.ok();
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody OnedayMaxInfo onedayMaxInfo) {
        serv.updateById(onedayMaxInfo);

        return R.ok();
    }

    /**
     * 删除
     */
    @DeleteMapping("/info/{id}")
    public R delete(@PathVariable String id) {
        serv.removeById(id);
        return R.ok();
    }


    @GetMapping("/getOnedayMax")
    public R getOnedayMax(@RequestParam(name = "lineId", required = false) Integer lineId,
                          @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                          @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<OnedayMaxInfo> page = new Page(curPage, size);

        serv.page(page, Wrappers.<OnedayMaxInfo>lambdaQuery().eq(OnedayMaxInfo::getLineId, lineId));
        return R.ok().put("data", page);
    }
}
