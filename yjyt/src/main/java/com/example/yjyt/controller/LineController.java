package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.LineInfo;
import com.example.yjyt.domain.LineInfoVO;
import com.example.yjyt.serv.LineInfoServ;
import com.example.yjyt.serv.impl.LineInfoServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RequestMapping("/line")
@RestController
public class LineController {

    @Autowired
    private LineInfoServImpl serv;

    @GetMapping("/table")
    public R table(@RequestParam(name = "key", required = false) String key,
                   @RequestParam(name = "pageNum", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "pageSize", required = false, defaultValue = "10") Integer size) {
        Page<LineInfoVO> page = new Page(curPage, size);
        serv.getPage(page, key);
        return R.ok().put("data", page);
    }

    @GetMapping("byLineId")
    public R getByLineId(@RequestParam(name = "lineId") Integer lineId) {
        LineInfoVO data = serv.getByLineId(lineId);
        return R.ok().put("data", data);
    }

    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") String id) {
        LineInfo lineInfo = serv.getById(id);
        return R.ok().put("data", lineInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody LineInfo lineInfo) {
        serv.save(lineInfo);

        return R.ok().put("data", lineInfo);
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody LineInfo lineInfo) {
        serv.updateById(lineInfo);

        return R.ok().put("data", lineInfo);
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
