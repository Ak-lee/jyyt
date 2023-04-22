package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.StringUtils;
import com.baomidou.mybatisplus.core.toolkit.Wrappers;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.ScheduleInfo;
import com.example.yjyt.domain.ScheduleInfoVO;
import com.example.yjyt.serv.ScheduleInfoServ;
import com.example.yjyt.serv.impl.ScheduleInfoImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.security.Key;
import java.sql.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RequestMapping("/schedule")
@RestController
public class ScheduleController {

    @Autowired
    private ScheduleInfoImpl serv;


    @GetMapping("/table")
    public R table(@RequestParam(name = "key", required = false) String key,
                   @RequestParam(name = "id", required = false) String id,
                   @RequestParam(name = "name", required = false) String name,
                   @RequestParam(name = "year", required = false) String year,
                   @RequestParam(name = "planType", required = false) String planType,
                   @RequestParam(name = "date1", required = false) String date1,
                   @RequestParam(name = "date2", required = false) String date2,
                   @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size) {
        Page<ScheduleInfo> page = new Page<>(curPage, size);
        LambdaQueryWrapper<ScheduleInfo> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(!StringUtils.isEmpty(key), ScheduleInfo::getLineId, key)
                .like(!StringUtils.isEmpty(id), ScheduleInfo::getId, id)
                .like(!StringUtils.isEmpty(name), ScheduleInfo::getName, name)
                .eq(!StringUtils.isEmpty(year), ScheduleInfo::getYear, year)
                .eq(!StringUtils.isEmpty(planType), ScheduleInfo::getPlanType, planType)
                .ge(!StringUtils.isEmpty(date1), ScheduleInfo::getStartTime, date1)
                .le(!StringUtils.isEmpty(date2), ScheduleInfo::getStartTime, date2);
        serv.page(page, wrapper);
        return R.ok().put("data", page);
    }

    /**
     * 信息
     */
    @GetMapping("/info/{id}")
    public R info(@PathVariable("id") String id) {
        ScheduleInfo scheduleInfo = serv.getById(id);
        return R.ok().put("data", scheduleInfo);
    }

    /**
     * 保存
     */
    @PostMapping
    public R save(@RequestBody ScheduleInfo scheduleInfo) {
        Integer lineId = scheduleInfo.getLineId();
        String planType = scheduleInfo.getPlanType();
        Date startDate = scheduleInfo.getStartTime();
        Date endDate = scheduleInfo.getEndTime();
        boolean exists = serv.isExists(lineId, planType, startDate, endDate);

        ScheduleInfo result = serv.getById(scheduleInfo.getId());
        if (result != null) {
            return R.error("id 已存在");
        } else if (exists) {
            return R.error("该计划与其他计划存在时间重叠");
        } else if (startDate == null || endDate == null) {
            return R.error("起止时间不能为空");
        } else {
            serv.save(scheduleInfo);
            return R.ok();
        }
    }

    /**
     * 修改
     */
    @PutMapping
    public R update(@RequestBody ScheduleInfo scheduleInfo) {
        serv.updateById(scheduleInfo);

        return R.ok();
    }

    @GetMapping("/tabledataall")
    public R tableAllWithPage(@RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                              @RequestParam(name = "size", required = false, defaultValue = "10") Integer size,
                              @RequestParam(name = "planType", required = true) String planType) {
        Page<ScheduleInfoVO> page = new Page<>(curPage, size);
        serv.getPage(page, planType);
        return R.ok().put("data", page);
    }


    @GetMapping("/tableDataAllNoPage")
    public R tableAllNoPage(@RequestParam(name = "planType", required = true) String planType) {
        Map<String, Object> map = new HashMap<>();
        map.put("plan_type", planType);
        return R.ok().put("list", serv.listByMap(map));
    }

    @GetMapping("/tableYearPlanNoPage")
    public R tableYearPlanNoPage() {
        return tableAllNoPage("年计划");
    }

    @GetMapping("/tableMonthPlanNoPage")
    public R tableMonthPlanNoPage() {
        return tableAllNoPage("月计划");
    }

    @GetMapping("/tableWeekPlanNoPage")
    public R tableWeekPlanNoPage() {
        return tableAllNoPage("周计划");
    }


    @GetMapping("/tabledata")
    public R table(@RequestParam(name = "key", required = false) Integer key,
                   @RequestParam(name = "curPage", required = false, defaultValue = "1") Integer curPage,
                   @RequestParam(name = "size", required = false, defaultValue = "10") Integer size,
                   @RequestParam(name = "planType", required = true) String planType) {
        Page<ScheduleInfoVO> page = new Page(curPage, size);
        serv.getPageByLineId(page, planType, key);
        return R.ok().put("data", page);
    }

    @GetMapping("/infoone/{id}")
    public R infoone(@PathVariable("id") String id) {
        ScheduleInfoVO scheduleInfoVO = serv.getOneById(id);
        return R.ok().put("data", scheduleInfoVO);
    }

    @PutMapping("/dispathByIds")
    public R dispathByIds(@RequestBody List<String> ids) {
        R result;
        boolean r = serv.dispatchByIds(ids);
        if (r) {
            result = R.ok();
        } else {
            result = R.error("失败");
        }
        return result;
    }

    /**
     * 删除
     */
    @DeleteMapping("/{id}")
    public R delete(@PathVariable String id) {
        // 删除的时候，不仅需要删除当前计划，还需要删除下属的所有计划。
        ScheduleInfoVO item = serv.getOneById(id);
        Date startTime = item.getStartTime();
        Date endTime = item.getEndTime();
        Integer lineId = item.getLineId();
        serv.removeById(id);
        QueryWrapper<ScheduleInfo> wrapper = new QueryWrapper<>();
        wrapper.eq("line_id", lineId);
        wrapper.between("start_time", startTime, endTime).or().between("end_time", startTime, endTime);
        serv.remove(wrapper);
        return R.ok();
    }
}
