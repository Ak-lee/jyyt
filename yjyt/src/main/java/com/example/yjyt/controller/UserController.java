package com.example.yjyt.controller;

import com.example.yjyt.common.R;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.*;

@RequestMapping("/user")
@RestController
// 这里并不直接处理登陆的问题，而是请求用户的登录信息
public class UserController {
    @Autowired
    private RestTemplate restTemplate;

    @GetMapping("/getInfo")
    public R getInfo(HttpServletRequest request,
                     HttpServletResponse response) throws JsonProcessingException {
        Cookie[] cookies = request.getCookies();
        List<String> cookiesList = new ArrayList<>();

        Arrays.asList(cookies).stream().forEach(i -> {
            String str = i.getName() + "=" + i.getValue();
            cookiesList.add(str);
        });
        HttpHeaders headers = new HttpHeaders();
        headers.put(HttpHeaders.COOKIE, cookiesList);
        HttpEntity<String> requestEntity = new HttpEntity<>(headers);

        ResponseEntity<String> forEntity = restTemplate.exchange("http://localhost:9999/user/getInfo", HttpMethod.GET, requestEntity, String.class);
        String rm = forEntity.getBody();
        return R.ok(rm);
    }
}
