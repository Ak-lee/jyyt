package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.*;
import com.example.yjyt.serv.impl.TasktypeDetailServiceImpl;
import com.example.yjyt.serv.impl.TypeInfoServImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RequestMapping("/tasktype")
@RestController
public class TaskTypeController {

    @Autowired
    private TypeInfoServImpl serv;

    @Autowired
    TasktypeDetailServiceImpl detailService;

    @GetMapping("/table")
    public R table(@RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<TaskTypeInfo> page = new Page(curPage, size);
        serv.page(page);
        return R.ok().put("data", page);
    }

    @GetMapping("/tableAll")
    public R tableAll() {
        return R.ok().put("data", serv.getAll());
    }


    @GetMapping("/getWithTasktypeDetail")
    public R getWithTasktypeDetail() {
        List<TaskTypeListVO> data = serv.getWithTasktypeDetail();
        return R.ok().put("data", data);
    }

    @GetMapping("/byTasktypeId")
    public R tableByTasktypeId(@RequestParam Long taskTypeId) {
        TaskTypeListVO data = serv.getListVOByTaskTypeId(taskTypeId);
        return R.ok().put("data", data);
    }

    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") String id) {
        TaskTypeInfo taskTypeInfo = serv.getById(id);

        return R.ok().put("data", taskTypeInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody TaskTypeInfo taskTypeInfo) {
        boolean save = serv.save(taskTypeInfo);
        Integer multiModeNum = taskTypeInfo.getMultiModeNum();
        multiModeNum = Math.max(1, multiModeNum);

        if (save) {
            ArrayList<TasktypeDetail> list = new ArrayList<>();
            for (int i = 0; i < multiModeNum; i++) {
                TasktypeDetail tasktypeDetail = new TasktypeDetail();
                tasktypeDetail.setTaskTypeId(taskTypeInfo.getId());
                list.add(tasktypeDetail);
            }
            detailService.saveBatch(list);
        }
        return R.ok();
    }


    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody TaskTypeInfo taskTypeInfo) {

        serv.updateById(taskTypeInfo);

        return R.ok();
    }

    @PutMapping("/updateDetail")
    public R updateDetail(@RequestBody TasktypeDetail tasktypeDetail) {
        detailService.updateById(tasktypeDetail);
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
