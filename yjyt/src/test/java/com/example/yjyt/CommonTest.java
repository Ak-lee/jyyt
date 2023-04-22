package com.example.yjyt;

import com.example.yjyt.domain.LineInfo;
import com.example.yjyt.domain.ScheduleContentHistory;
import com.example.yjyt.domain.TaskTypeInfo;
import com.example.yjyt.exception.BusinessException;
import com.example.yjyt.mapper.LineMapper;
import com.example.yjyt.mapper.TaskTypeMapper;
import com.example.yjyt.serv.impl.LineInfoServImpl;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CommonTest {
    @Autowired
    private TaskTypeMapper mapper;

    public void getList() {
        List<TaskTypeInfo> a = mapper.selectList(null);
    }

    @Test
    public void test2() {
//        String overhaulPlanName = "SFM64-均衡修14B-2-17009";
//        String[] split = overhaulPlanName.split("-");
//        List<String> list = Arrays.asList(split);
//        System.out.println(list);
//        ScheduleContentHistory item = new ScheduleContentHistory();
//        if (list.get(1).contains("均衡修")) {
//            String regEx = "[^0-9]";
//            Pattern p = Pattern.compile(regEx);
//            Matcher m = p.matcher(list.get(1));
//
//            String month = m.replaceAll("").trim();
//            String content = list.get(1).substring(list.get(1).indexOf(month));
//            System.out.println(month);
//            System.out.println(content);
//            item.setApplyMonth(Integer.valueOf(month));
//            item.setPerformDate();
//        }
    }
}
