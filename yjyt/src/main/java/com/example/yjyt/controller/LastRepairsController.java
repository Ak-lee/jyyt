package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.LastRepairInfo;
import com.example.yjyt.domain.OnedayMaxInfo;
import com.example.yjyt.serv.impl.LastRepairInfoServImpl;
import com.example.yjyt.serv.impl.OnedayMaxServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RequestMapping("/lastRespairs")
@RestController
public class LastRepairsController {

    @Autowired
    private LastRepairInfoServImpl serv;

    @GetMapping("/table")
    public R table(@RequestParam(name = "key", required = false) String key,
                   @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<LastRepairInfo> page = new Page(curPage, size);
        serv.page(page, Wrappers.<LastRepairInfo>lambdaQuery().like(key != null, LastRepairInfo::getId, key));
        return R.ok().put("data", page);
    }


    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") String id) {
        LastRepairInfo lastRepairInfo = serv.getById(id);

        return R.ok().put("data", lastRepairInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody LastRepairInfo lastRepairInfo) {
        serv.save(lastRepairInfo);
        return R.ok();
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody LastRepairInfo lastRepairInfo) {
        serv.updateById(lastRepairInfo);

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



    @GetMapping("/getlastRepairs")
    public R getlastRepairs(@RequestParam(name = "lineId", required = false) Integer lineId,
                          @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                          @RequestParam(name = "size", required = false, defaultValue = "10") Integer size){
        Page<LastRepairInfo> page = new Page<>(curPage, size);

        serv.page(page, Wrappers.<LastRepairInfo>lambdaQuery().eq(LastRepairInfo::getLineId,lineId));
        return R.ok().put("data", page);

    }
}
