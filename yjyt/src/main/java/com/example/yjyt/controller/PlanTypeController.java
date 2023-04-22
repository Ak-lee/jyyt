package com.example.yjyt.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.PlanTypeInfo;
import com.example.yjyt.domain.PlanTypeInfoVO;
import com.example.yjyt.serv.impl.PlanTypeServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RequestMapping("/plantype")
@RestController
public class PlanTypeController {

    @Autowired
    private PlanTypeServImpl serv;

    @GetMapping("/table")
    public R tableAll(@RequestParam(name = "pageNum", required = false, defaultValue = "1") Integer curPage,
                      @RequestParam(name = "pageSize", required = false, defaultValue = "10") Integer size) {
        Page<PlanTypeInfoVO> page = new Page(curPage, size);
        serv.getPage(page);
        return R.ok().put("data", page);
    }

    @GetMapping("/table/{lineId}")
    public R table(@PathVariable Integer lineId,
                   @RequestParam(name = "pageNum", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "pageSize", required = false, defaultValue = "10") Integer size) {
        Page<PlanTypeInfoVO> page = new Page(curPage, size);
        serv.getPageByLineId(page, lineId);
        return R.ok().put("data", page);
    }


    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") String id) {
        PlanTypeInfo planTypeInfo = serv.getById(id);
        return R.ok().put("data", planTypeInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody PlanTypeInfo planTypeInfo) {
        serv.save(planTypeInfo);

        return R.ok().put("data", planTypeInfo);
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody PlanTypeInfo planTypeInfo) {
        serv.updateById(planTypeInfo);

        return R.ok().put("data", planTypeInfo);
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
