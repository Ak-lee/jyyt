package com.example.yjyt.controller;

import com.example.yjyt.common.R;
import com.example.yjyt.domain.ApplyMonth;
import com.example.yjyt.domain.ApplyMonthVO;
import com.example.yjyt.serv.impl.ApplyMonthServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/applyMonth")
@RestController
public class ApplyMonthController {
    @Autowired
    private ApplyMonthServiceImpl serv;

    @GetMapping("/table")
    public R table(@RequestParam(name = "tasktypeId") Long tasktypeId) {
        List<ApplyMonthVO> list = serv.table(tasktypeId);
        return R.ok().put("data", list);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody ApplyMonth applyMonth) {
        serv.save(applyMonth);
        return R.ok().put("data", applyMonth);
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody ApplyMonth applyMonth) {
        serv.updateById(applyMonth);

        return R.ok().put("data", applyMonth);
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