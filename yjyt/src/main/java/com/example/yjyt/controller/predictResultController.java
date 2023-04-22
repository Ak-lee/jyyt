package com.example.yjyt.controller;

import com.example.yjyt.common.R;
import com.example.yjyt.domain.predResult;
import com.example.yjyt.serv.impl.ForcastPictureServiceImpl;
import com.example.yjyt.serv.impl.predResultsServImpl;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/mileage_history")
public class predictResultController {
    @Resource
    private predResultsServImpl serv;

    @Resource
    private ForcastPictureServiceImpl serv2;

    @RequestMapping("/getPredres")
    public Map<String, Object> getPredresPages() {
        List<predResult> predResInfoList = serv.getPredResultList();
        List<predResult> getendTrainingList = serv.gettrainingEndtimes();
        Map<String, Object> res = new HashMap<>();
        res.put("data", predResInfoList);
        res.put("endTrain", getendTrainingList);
        return res;
    }

    @RequestMapping("/getPredImg")
    public String getPredImg(@RequestParam("trainId") String trainId) {
        return serv2.getPredImg(trainId);
    }
}
