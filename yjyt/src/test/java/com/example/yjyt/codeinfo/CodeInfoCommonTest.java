package com.example.yjyt.codeinfo;

import com.example.yjyt.codeinfo.serv.CodeInfoServ;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class CodeInfoCommonTest {
    @Autowired
    private CodeInfoServ codeInfoServ;

    public void getCodeTest() {
        String test = codeInfoServ.getCode("station_info");
        System.out.println("test:" + test);
        test = codeInfoServ.getCode("station_info");
        System.out.println("test:" + test);
        test = codeInfoServ.getCode("station_info");
        System.out.println("test:" + test);
    }
}
