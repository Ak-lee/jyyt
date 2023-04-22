
package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.*;
import com.example.yjyt.serv.impl.YardTasktypeMapperServiceImpl;
import com.example.yjyt.util.CopyUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RequestMapping("/yardTasktype")
@RestController
public class YardTasktypeController {

    @Autowired
    private YardTasktypeMapperServiceImpl serv;

    @GetMapping("/byYard")
    // 查询该车场支持的检修任务类型
    public R tableByYardId(@RequestParam String yardId) {
        List<YardTaskTypeListVO> data = serv.getByYardId(yardId);
        return R.ok().put("data", data);
    }

    @GetMapping("/byYardIdAndTasktypeId")
    // 根据车场id和检修任务类型Id，获取多修程的子修程的数量。
    public R tableByYardIdAndTasktypeId(@RequestParam String yardId, @RequestParam Long taskTypeId) {
        YardTaskTypeListVO data = serv.getListVOByYardIdAndTaskTypeId(yardId, taskTypeId);
        return R.ok().put("data", data);
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody YardTasktype item) {
        QueryWrapper<YardTasktype> wrapper = new QueryWrapper<>();
        wrapper.eq("yard_id", item.getYardId());
        wrapper.eq("tasktype_id",item.getTasktypeId());
        serv.update(wrapper);
        return R.ok();
    }

    @PostMapping
    public R add(@RequestBody YardTasktype item) {
        serv.save(item);
        return R.ok();
    }

    @PostMapping("/batch")
    public R saveBatch(@RequestBody YardTaskTypeDTO dto) {
        String id = dto.getYardId();
        Map<String, Object> map = new HashMap<>();
        map.put("yard_id", id);
        serv.removeByMap(map);
        List<YardTasktype> list = CopyUtil.copyList(dto.getList(), YardTasktype.class);
        serv.saveBatch(list);
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
