package com.example.yjyt.controller;

import com.example.yjyt.common.R;
import com.example.yjyt.domain.ForcastMileage;
import com.example.yjyt.serv.impl.ForcastMileageServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.sql.Date;
import java.util.List;

@RequestMapping("/mileageForecast")
@RestController
public class MileageForecast {
    @Autowired
    private ForcastMileageServiceImpl serv;

    @GetMapping("/getByTrainIdAndDate")
    public R getItemByTrainIdAndDate(@RequestParam(name = "trainId") String trainId, @RequestParam(name = "date") Date date) {
        ForcastMileage data = serv.getItemByTrainIdAndDate(trainId, date);
        return R.ok().put("data", data);
    }

    @GetMapping("/getByTrainIdAndRange")
    public R getByTrainIdAndRange(@RequestParam(name = "trainId") String trainId,
                                  @RequestParam(name = "sdate") Date sdate,
                                  @RequestParam(name = "edate") Date edate
    ) {
        List<ForcastMileage> data = serv.getByTrainIdAndRange(trainId, sdate, edate);
        return R.ok().put("data", data);
    }

    @GetMapping("/table")
    public R table() {
        List<ForcastMileage> list = serv.list();
        return R.ok().put("list", list);
    }
}
