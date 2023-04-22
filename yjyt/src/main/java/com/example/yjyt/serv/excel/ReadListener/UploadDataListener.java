package com.example.yjyt.serv.excel.ReadListener;

import com.alibaba.excel.context.AnalysisContext;
import com.alibaba.excel.read.listener.ReadListener;
import com.example.yjyt.domain.excel.ResultData;
import com.example.yjyt.domain.excel.UploadData;
import com.example.yjyt.mapper.MileageHistoryMapper;
import com.example.yjyt.mapper.TrainMapper;
import lombok.extern.slf4j.Slf4j;

import java.util.*;


// dataListener 不能被 Spring 管理，要每次读取 excel 都要 new，然后里面用到 spring 可以构造方法传进去
@Slf4j
public class UploadDataListener implements ReadListener<UploadData> {

    private List<ResultData> resultList = new ArrayList<>();

    private Set<UploadData> uploadDataSet = new HashSet<>();

    private MileageHistoryMapper mileageHistoryMapper;

    private TrainMapper trainMapper;

    public UploadDataListener() {   // 无参构造函数
    }

    /***
     * 如果使用了 spring ，请使用这个构造方法。每次创建 Listener 的时候需要把 spring 管理的类传进来。
     */
    public UploadDataListener(MileageHistoryMapper mileageHistoryMapper, TrainMapper trainMapper) {
        this.mileageHistoryMapper = mileageHistoryMapper;
        this.trainMapper = trainMapper;
    }

    /**
     * 这个每一条数据解析都会来调用。
     */
    @Override
    public void invoke(UploadData data, AnalysisContext context) {
//        log.info("解析到一条数据：{}", JSON.toJSONString(data));
//
//        Map<String, Object> map = new HashMap<>();
//        map.put("train_id", data.getTrainId());
//        map.put("date", data.getDate());
//        List<MileageHistory> historyItems = mileageHistoryMapper.selectByMap(map);
//        MileageHistory history = null;
//        if (historyItems.size() > 0) {
//            history = historyItems.get(0);
//        }
//        ResultData result = new ResultData();
//        result.setRowIndex(context.readRowHolder().getRowIndex());
//
//        TrainInfo trainInfo = trainMapper.selectById(data.getTrainId());
//        if (trainInfo == null) {
//            log.info("该列车不存在");
//            result.setType("该列车不存在");
//        } else {
//            // excel 数据与数据库数据对比
//            if (history == null) {   // 新增数据
//                result.setType("新增");
//            } else {
//                if (history.getMileage() == data.getMileage()) {    // 重复数据
//                    result.setType("excel与数据库重复");
//                } else {    // 冲突数据
//                    result.setType("冲突");
//                }
//            }
//        }
//        // excel 之间对比（判重复）
//        if (!uploadDataSet.add(data)) {
//            // excel 数据内部发生重复
//            result.setType("excel内重复");
//        }
//
//        log.info("准备向前端返回一条数据{}", result);
//        resultList.add(result);
    }

    /**
     * 所有数据解析完成了，都会来调用
     */
    @Override
    public void doAfterAllAnalysed(AnalysisContext context) {
        log.info("所有数据解析完成！");
    }

    public List<ResultData> getList() {
        return resultList;
    }

    @Override
    public void onException(Exception exception, AnalysisContext context) {
//        log.error("解析失败，但是继续解析下一行:{}", exception.getMessage());
//        // 如果是某一个单元格的转换异常 能获取到具体行号
//        if (exception instanceof ExcelDataConvertException) {
//            ExcelDataConvertException excelDataConvertException = (ExcelDataConvertException) exception;
//            log.error("第{}行，第{}列解析异常，数据为:{}", excelDataConvertException.getRowIndex(),
//                    excelDataConvertException.getColumnIndex(), excelDataConvertException.getCellData());
//
//            log.error("解析错误数据详情: ", excelDataConvertException.getExcelContentProperty());
//            log.error("解析错误数据详情: ", excelDataConvertException.getCellData().getStringValue());
//            Object o = context.readRowHolder().getCellMap().get(excelDataConvertException.getColumnIndex());
//            log.error("解析错误数据详情: ", o);
//
//            resultList.add(new ResultData(excelDataConvertException.getRowIndex(), "解析异常"));

    }
}