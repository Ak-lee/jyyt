
package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.TeamInfo;
import com.example.yjyt.serv.impl.TeamInfoServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequestMapping("/team")
@RestController
public class TeamController {

    @Autowired
    private TeamInfoServImpl serv;

    @GetMapping("/table")
    public R table(@RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<TeamInfo> page = new Page(curPage, size);
        serv.page(page, Wrappers.<TeamInfo>lambdaQuery());
        return R.ok().put("data", page);
    }

    @GetMapping("/tableall")
    public R tableAll() {
        return R.ok().put("data", serv.getAll());
    }

    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") String id) {
        TeamInfo teamInfo = serv.getById(id);

        return R.ok().put("data", teamInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody TeamInfo teamInfo) {
        serv.save(teamInfo);

        return R.ok();
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody TeamInfo teamInfo) {
        serv.updateById(teamInfo);

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
