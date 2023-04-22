package com.example.yjyt.serv.excel;

import com.example.yjyt.domain.MileageHistory;
import com.example.yjyt.domain.TrainInfo;
import com.example.yjyt.domain.excel.ResultData;
import com.example.yjyt.domain.excel.UploadData;
import com.example.yjyt.mapper.MileageHistoryMapper;
import com.example.yjyt.mapper.TrainMapper;
import com.example.yjyt.serv.impl.MileageHistoryServImpl;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
@Slf4j
public class UploadService {
//    @Autowired
//    private DatabaseService databaseService;

    @Autowired
    private MileageHistoryServImpl mileageHistoryServImpl;

    @Autowired
    private MileageHistoryMapper mileageHistoryMapper;
    @Autowired
    private TrainMapper trainMapper;

    public Integer saveBatch(List<MileageHistory> list) {
        Integer count = mileageHistoryServImpl.saveMileageHistory(list);
        return count;
    }

    public List<ResultData> reviewData(List<UploadData> list) {
        List<ResultData> resultList = new ArrayList<>();
        Set<UploadData> uploadDataSet = new HashSet<>();

        for (int i = 0; i < list.size(); i++) {
            UploadData item = list.get(i);
            ResultData result = new ResultData();

            // excel 之间对比（判重复）
            if (!uploadDataSet.add(item)) {
                // excel 数据内部发生重复
                result.setId(item.getId());
                result.setType("excel内重复");
            }
            if(result.getType()==null || (!result.getType().equals("excel内重复"))) {
                result=reviewItem(item);
            }

            resultList.add(result);
            log.info("准备向前端返回一条数据{}", result);
        }
        return resultList;
    }

    public ResultData reviewItem(UploadData data) {
        ResultData result = new ResultData();
        Map<String, Object> map = new HashMap<>();
        map.put("train_id", data.getTrainId());
        map.put("date", data.getDate());

        List<MileageHistory> historyItems = mileageHistoryMapper.selectByMap(map);
        MileageHistory history = null;
        if (historyItems.size() > 0) {
            history = historyItems.get(0);
        }

        result.setId(data.getId());
        TrainInfo trainInfo = trainMapper.selectById(data.getTrainId());
        if (trainInfo == null) {
            log.info("该列车不存在");
            result.setType("该列车不存在");
        } else {
            // excel 数据与数据库数据对比
            if (history == null) {   // 新增数据
                result.setType("新增");
            } else {
                if (history.getMileage() == data.getMileage()) {    // 重复数据
                    result.setType("excel与数据库重复");
                } else {    // 冲突数据
                    result.setType("冲突");
                }
            }
        }
        return result;
    }
}
