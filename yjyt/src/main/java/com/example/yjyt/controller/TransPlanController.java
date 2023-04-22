package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.Query;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.TransPlanInfo;

import com.example.yjyt.serv.impl.TransPlanInfoServImpl;
import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Date;
import java.util.List;

@RequestMapping("/transplan")
@RestController
public class TransPlanController {

    @Autowired
    private TransPlanInfoServImpl serv;

    @GetMapping("/table")
    public R table(@RequestParam(name = "key", required = false) String key,
                   @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<TransPlanInfo> page = new Page(curPage, size);
        serv.page(page, Wrappers.<TransPlanInfo>lambdaQuery().like(key != null, TransPlanInfo::getId, key));
        return R.ok().put("data", page);
    }

    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") String id) {
        TransPlanInfo transPlanInfo = serv.getById(id);

        return R.ok().put("data", transPlanInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody TransPlanInfo transPlanInfo) {
        serv.save(transPlanInfo);
        return R.ok();
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody TransPlanInfo transPlanInfo) {
        serv.updateById(transPlanInfo);

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


    @GetMapping("/getTransPlan")//传两个参数
    public R getTransPlan(@RequestParam(name = "lineId", required = false) Integer lineId,
                          @RequestParam(name = "applicableTime", required = false) String applicableTime,
                          @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                          @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<TransPlanInfo> page = new Page(curPage, size);

        serv.page(page, Wrappers.<TransPlanInfo>lambdaQuery().and(i -> i.eq(TransPlanInfo::getLineId, lineId).eq(TransPlanInfo::getApplicableTime, applicableTime)));
        return R.ok().put("data", page);
    }

    @GetMapping("/getTransPlan2")//传两个参数
    public R getTransPlan2(@RequestParam(name = "lineId", required = false) Integer lineId,
                           @RequestParam(name = "applicableTime", required = false) String applicableTime) {
        QueryWrapper<TransPlanInfo> wrapper = new QueryWrapper<>();
        wrapper.eq("line_id", lineId);
        wrapper.eq("applicable_time", applicableTime);
        wrapper.orderBy(true, true, "inyard_time");
        List<TransPlanInfo> list = serv.list(wrapper);
        return R.ok().put("data", list);
    }
}
