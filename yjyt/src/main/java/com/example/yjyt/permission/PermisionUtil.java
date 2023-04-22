package com.example.yjyt.permission;

import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import java.util.*;

@Component
public class PermisionUtil {
    @Autowired
    private RestTemplate restTemplate;

//    public boolean hasPermission(HttpServletRequest request, String lineId) throws JsonProcessingException {
//        // 根据 request 获取用户的cookie，查看用户的信息，判断用户是否有权限访问
//        JSONObject info = this.getInfo(request);
//        if (info == null) return false;
//        if((int)info.get("code") != 0) {
//            return false;
//        }
//
//    }

    public JSONObject getInfo(HttpServletRequest request) throws JsonProcessingException {
        Cookie[] cookies = request.getCookies();

        Optional<Cookie> first = Arrays.stream(cookies).filter(i -> Objects.equals(i.getName(), "sid")).findFirst();

        if (!first.isPresent()) {
            return null;
        }

        ResponseEntity<JSONObject> forEntity = restTemplate.getForEntity("10.73.82.158:8001/auth/userinfoSession?sid=" + first.get(), JSONObject.class);
        return forEntity.getBody();
    }

//    public String convertLineNameToLineId(String lineName) {
//        // lineName : 成都 18 号线，
//        // 转换为 lineId: CD18
//
//    }
}
