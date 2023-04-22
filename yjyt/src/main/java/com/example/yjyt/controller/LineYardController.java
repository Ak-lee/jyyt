package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.LineYardInfo;
import com.example.yjyt.domain.LineYardInfoDTO;
import com.example.yjyt.serv.impl.LineYardInfoServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.example.yjyt.util.CopyUtil;

@RequestMapping("/lineyard")
@RestController
public class LineYardController {

    @Autowired
    private LineYardInfoServImpl serv;

    @GetMapping("/table")
    public R table(@RequestParam(name = "key", required = false) String key,
                   @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<LineYardInfo> page = new Page(curPage, size);
        serv.page(page, Wrappers.<LineYardInfo>lambdaQuery().like(key != null, LineYardInfo::getLineId, key));//如果给了线路id，根据线路查该线路对应得车场
        return R.ok().put("data", page);
    }


    /**
     * 信息
     */
    @GetMapping("/info/{lineId}/{yardId}")
    public R info(@PathVariable("lineId") String lineId,
                  @PathVariable("yardId") String yardId) {
        LineYardInfo lineYardInfo = null;
        LambdaQueryWrapper<LineYardInfo> Wrapper = new LambdaQueryWrapper<>();
        Wrapper.and(i -> i.eq(LineYardInfo::getLineId, lineId).eq(LineYardInfo::getYardId, yardId));
        if (!serv.list(Wrapper).isEmpty()) {
            lineYardInfo = serv.list(Wrapper).get(0);
        }
        return R.ok().put("data", lineYardInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody LineYardInfo LineYardInfo) {
        serv.save(LineYardInfo);

        return R.ok();
    }

    /**
     * 批量保存，上传的都是同一个线路的更新后的车场
     * 直接把该线路之前的所有车场删除，新添加上传的车场列别
     */
    @PostMapping("/batch")
    public R saveBatch(@RequestBody LineYardInfoDTO dto) {
        int id = dto.getLineId();
        Map<String, Object> map = new HashMap<>();
        map.put("line_id", id);
        serv.removeByMap(map);
        List<LineYardInfo> list = CopyUtil.copyList(dto.getList(), LineYardInfo.class);
        serv.saveBatch(list);
        return R.ok();
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody LineYardInfo LineYardInfo) {
        serv.updateById(LineYardInfo);

        return R.ok();
    }

    /**
     * 删除
     */
    @DeleteMapping
    public R delete(@RequestParam Integer lineId, @RequestParam String yardId) {
        Map<String, Object> map = new HashMap<>();
        map.put("lineId", lineId);
        map.put("yardId", yardId);
        serv.removeByMap(map);
        return R.ok();
    }
}
