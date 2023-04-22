package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.example.yjyt.common.R;
import com.example.yjyt.domain.*;
import com.example.yjyt.serv.impl.ForcastMileageServiceImpl;
import com.example.yjyt.serv.impl.MileageHistoryServImpl;
import com.example.yjyt.serv.impl.ScheduleContentHistoryImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.sql.Date;
import java.util.*;

@RestController
@RequestMapping("/mileage_history")
public class MileageHistoryController {
    @Autowired
    MileageHistoryServImpl serv;

    @Autowired
    private ScheduleContentHistoryImpl serv2;

    @Autowired
    ForcastMileageServiceImpl forcastServ;

    @GetMapping("/table")
    public R table(@RequestParam(name = "lineId") Integer lineId,
                   @RequestParam(name = "sdate") Date sdate,
                   @RequestParam(name = "edate") Date edate) {
        List<MileageHistory> list = serv.getMileageList(lineId, sdate, edate);
        return R.ok().put("data", list);
    }

    @GetMapping("/getByTrainIdAndDate")
    public R getItemByTrainIdAndDate(@RequestParam(name = "trainId") String trainId,
                                     @RequestParam(name = "date") Date date) {
        MileageHistory data = serv.getItemByTrainIdAndDate(trainId, date);
        if (data != null) {
            return R.ok().put("data", data);
        } else {
            ForcastMileage data2 = forcastServ.getItemByTrainIdAndDate(trainId, date);
            return R.ok().put("data", data2);
        }
    }

    @GetMapping("/getByTrainIdAndSDateAndEDate")
    public R getByTrainIdAndSDateAndEDate(@RequestParam(name = "trainId") String trainId,
                                          @RequestParam(name = "sdate") Date sdate,
                                          @RequestParam(name = "edate") Date edate
    ) throws Exception {
        Calendar calendar = new GregorianCalendar();
        calendar.setTime(sdate);

        Calendar calendar2 = new GregorianCalendar();
        calendar2.setTime(edate);

        if (calendar.after(calendar2)) {
            throw new Exception("时间范围不正确");
        }

        ArrayList<MileageHistory> arr = new ArrayList<>();

        Date date;

        while (!calendar.after(calendar2)) {
            date = new Date(calendar.getTime().getTime());
            R item = this.getItemByTrainIdAndDate(trainId, date);

            MileageHistory result = (MileageHistory) item.get("data");
            arr.add((MileageHistory) item.get("data"));
            calendar.add(Calendar.DATE, 1);
        }
        return R.ok().put("list", arr);
    }


    @GetMapping("/getPagesOverview")
    public R getPagesOverview(@RequestParam(name = "lineId") Integer lineId) {
        Map<String, java.util.Date> result = serv.getPagesOverview(lineId);
        return R.ok().put("data", result);
    }

    @GetMapping("/getDiffBylineIdAndDate")
    public R getBylineIdAndDate(@RequestParam(name = "lineId") Integer lineId,
                                @RequestParam(name = "date") Date date
    ) {
        // 根据线路id，和日期，查询该线路下所有列车自上次检修到现在已经运行了多少里程。
        List<ScheduleContentHistory> scheduleContentHistories = serv2.lastAnyTypeRepairByLineId(lineId, date);
        List<MileageHistoryDiff> arr = new ArrayList<>();
        scheduleContentHistories.forEach(i -> {
            Date performDate = new Date(i.getPerformDate().getTime());
            String trainId = i.getTrainId();

            MileageHistory prevItem = serv.getItemByTrainIdAndDate(trainId, performDate);
            MileageHistory curItem = serv.getItemByTrainIdAndDate(trainId, date);


            if (Objects.nonNull(prevItem) && Objects.nonNull(curItem)) {
                MileageHistoryDiff item = new MileageHistoryDiff(trainId,
                        curItem.getMileage() - prevItem.getMileage());
                arr.add(item);
            }
        });
        return R.ok().put("list", arr);
    }

    @PutMapping
    public R update(@RequestBody List<MileageHistoryDTO> list) {
        // 这里的 PUT 逻辑，不仅要处理 更新，还要处理 添加。
        List<MileageHistory> updateList = new ArrayList<>();
        List<MileageHistory> addList = new ArrayList<>();

        list.forEach(item -> {
            if (Objects.equals(item.getType(), "插值")) {
                addList.add(item);
            } else {
                updateList.add(item);
            }
        });
        if (!addList.isEmpty()) {
            serv.saveBatch(addList);
        }
        if (!updateList.isEmpty()) {
            updateList.forEach(item -> {
                QueryWrapper<MileageHistory> wrapper = new QueryWrapper<>();
                wrapper.eq("train_id", item.getTrainId());
                wrapper.eq("date", item.getDate());
                serv.update(item, wrapper);
            });
        }

        return R.ok();
    }

    @PostMapping
    public R save(@RequestBody List<MileageHistory> list) {
        serv.saveBatch(list);
        return R.ok();
    }
}
