package com.example.yjyt.codeinfo.serv;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.example.yjyt.codeinfo.domain.CodeInfo;
import com.example.yjyt.codeinfo.domain.dto.CodeDTO;
import com.example.yjyt.codeinfo.domain.vo.Segment;

import java.util.List;

public interface CodeInfoServ {

    JSONObject previewExpression(List<Segment> segments);


    CodeInfo findById(String id);

    void add(CodeInfo dto);

    void update(CodeDTO dto);

    void start(String id);

    void stopById(String id);

    String genCode(String expression, Integer flowNum);

    void deleteById(String id);

    String getCode(String className);

    JSONArray getCurrentOptions();

    void enable(String id);

    void disable(String id);

    JSONArray getIdNames();

    List<Segment> getInputBox(String id);

    String getFinalCode(String id, List<Segment> segs);
}
