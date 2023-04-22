package com.example.yjyt;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.yjyt.domain.LineInfo;
import com.example.yjyt.mapper.LineMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.sql.Date;
import java.util.List;

@SpringBootTest
class YjytApplicationTests {
    @Autowired
    private LineMapper lineMapper;

    void contextLoads() {
        //List<LineInfo> list = lineMapper.selectList(null);
        //设置分页参数
        Page<LineInfo> page = new Page<>(2, 1);//注意这里第一个参数表示第几页，它只显示该页数据
        lineMapper.selectPage(page, null);
        //获取分页数据
        List<LineInfo> list = page.getRecords();//将所有记录数得到
    }
}
