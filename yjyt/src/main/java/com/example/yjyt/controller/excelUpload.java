package com.example.yjyt.controller;

import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.example.yjyt.domain.MileageHistory;
import com.example.yjyt.domain.UpdateMileageHistoryDTO;
import com.example.yjyt.domain.excel.ResultData;
import com.example.yjyt.domain.excel.UploadData;
import com.example.yjyt.mapper.MileageHistoryMapper;
import com.example.yjyt.mapper.TrainMapper;
import com.example.yjyt.serv.impl.MileageHistoryServImpl;
import com.example.yjyt.serv.excel.UploadService;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;


import java.util.*;

@RestController
@AllArgsConstructor
@Slf4j
@RequestMapping("/excel")
public class excelUpload {
    @Autowired
    private UploadService uploadService;

    @Autowired
    private MileageHistoryServImpl mileageHistorySerImpl;

    @Autowired
    private MileageHistoryMapper mileageHistoryMapper;
    @Autowired
    private TrainMapper trainMapper;

    @PostMapping("/saveBatch")
    public Integer save(@RequestBody List<MileageHistory> uploadDataList) {
        int count = uploadService.saveBatch(uploadDataList);
        return count;
    }

    @PostMapping("/saveItem")
    public String saveItem(@RequestBody MileageHistory uploadData) {
        mileageHistorySerImpl.save(uploadData);
        return "success";
    }

    @PostMapping("/review")
    public List<ResultData> reviewData(@RequestBody List<UploadData> uploadDataList) {
        return uploadService.reviewData(uploadDataList);
    }

    @PostMapping("/reviewItem")
    public ResultData reviewItem(@RequestBody UploadData uploadDataList) {
        return uploadService.reviewItem(uploadDataList);
    }

    @PostMapping("/updateItem")
    public boolean updateItem(@RequestBody UpdateMileageHistoryDTO DTO) {
        UpdateWrapper<MileageHistory> updateWrapper = new UpdateWrapper<>();
        updateWrapper.eq("train_id", DTO.getMileageHistory().getTrainId())
                .eq("date", DTO.getMileageHistory().getDate());
        return mileageHistorySerImpl.update(DTO.getMileageHistory(), updateWrapper);
    }

    @DeleteMapping("/deleteItem")
    public int deleteItem(@RequestBody UploadData data) {
        Map<String, Object> map = new HashMap<>();
        map.put("train_id", data.getTrainId());
        map.put("date", data.getDate());
        return mileageHistoryMapper.deleteByMap(map);
    }
}
