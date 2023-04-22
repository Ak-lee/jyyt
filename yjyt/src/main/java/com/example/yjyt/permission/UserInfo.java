package com.example.yjyt.permission;

import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
public class UserInfo {
    @Autowired
    private RestTemplate restTemplate;

    public JSONObject getInfo(HttpServletRequest request,
                              HttpServletResponse response) throws JsonProcessingException {
        Cookie[] cookies = request.getCookies();
        List<String> cookiesList = new ArrayList<>();

        Arrays.asList(cookies).stream().forEach(i -> {
            String str = i.getName() + "=" + i.getValue();
            cookiesList.add(str);
        });
        HttpHeaders headers = new HttpHeaders();
        headers.put(HttpHeaders.COOKIE, cookiesList);
        HttpEntity<JSONObject> requestEntity = new HttpEntity<>(headers);

        ResponseEntity<JSONObject> forEntity = restTemplate.exchange("http://localhost:9999/user/getInfo", HttpMethod.GET, requestEntity, JSONObject.class);
        return forEntity.getBody();
    }
}
