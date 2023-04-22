package com.example.yjyt.util;

import com.alibaba.excel.EasyExcel;
import com.alibaba.excel.support.ExcelTypeEnum;
import com.alibaba.excel.write.builder.ExcelWriterBuilder;
import com.alibaba.fastjson.JSON;
import org.springframework.stereotype.Component;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


@Component
public class ExcelUtils {
    /**
     * 导出excel
     *
     * @param objects 数据List
     * @param response 返回response对象
     * @param fileName 返回文件的名称
     * @param c 数据List的对象类
     */
    public <T> void excelExport(List<?> objects, HttpServletResponse response, String fileName, Class<T> c) throws IOException {
        if (objects.size() == 0)
            return;
        ServletOutputStream outputStream = null;
        try {
//            response.setContentType("application/vnd.ms-excel;charset=utf-8");
            response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8");
            response.setCharacterEncoding("utf-8");
            response.setHeader("Content-disposition", "attachment;filename=" + new String(fileName.getBytes(), "ISO8859-1") + ".xlsx");
            outputStream = response.getOutputStream();
            ExcelWriterBuilder write = EasyExcel.write(response.getOutputStream(), c).excelType(ExcelTypeEnum.XLSX);
            write.sheet(fileName).doWrite(objects);
            if (outputStream != null) {
                outputStream.close();
            }
        } catch (Exception e) {
            response.reset();
            response.setContentType("application/json");
//            response.setContentType("application/blob");
//            blob

            response.setCharacterEncoding("utf-8");
            Map<String, Object> map = new HashMap<>();
            map.put("code", 500);
            map.put("msg", "下载文件失败" + e.getMessage());
            map.put("data", null);
            response.getWriter().println(JSON.toJSONString(map));
        }
    }
}
