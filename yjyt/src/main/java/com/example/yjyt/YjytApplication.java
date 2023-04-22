package com.example.yjyt;

import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;

import java.text.DateFormat;
import java.util.Date;

@EnableScheduling
@SpringBootApplication
@Slf4j
@MapperScan(basePackages = {"com.example.yjyt.mapper", "com.example.yjyt.**.dao"})
public class YjytApplication {
    public static void main(String[] args) {
        SpringApplication.run(YjytApplication.class, args);
        log.info("\\n\\n\\n\\n\\n\\n\\n\\n\n\n\nヾ(◍°∇°◍)ﾉﾞ   启动成功");
    }

    // 我们的定时任务 半小时提醒一次, 固定间隔 每半分钟执行一次
//    @Scheduled(fixedRate = 1 * 30 * 1000)
//    public void playSth() {
//        System.out.println("定时任务测试，，，，" +
//                DateFormat.getDateTimeInstance().format(new Date()));
//    }
    @Autowired
    private SqlSessionFactory sqlSessionFactory;
}
