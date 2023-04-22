package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.YardShifts;
import com.example.yjyt.serv.impl.ShiftsServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/shifts")
public class YardShiftsController {
    @Autowired
    private ShiftsServiceImpl serv;

    @GetMapping("/table")
    public R tableAll(@RequestParam String yardId) {
        QueryWrapper<YardShifts> wrapper = new QueryWrapper<>();
        wrapper.eq("yard_id", yardId);

        List<YardShifts> list = serv.list(wrapper);
        return R.ok().put("data", list);
    }

    @PostMapping("/")
    public R saveItem(@RequestBody YardShifts shift) {
        Boolean result = serv.save(shift);
        return R.ok().put("result", result);
    }

    @PutMapping("/")
    public R updateItem(@RequestBody YardShifts shift) {
        QueryWrapper<YardShifts> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("id", shift.getId());
        boolean result = serv.update(shift, queryWrapper);
        if (result) {
            return R.saveOk(shift);
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
