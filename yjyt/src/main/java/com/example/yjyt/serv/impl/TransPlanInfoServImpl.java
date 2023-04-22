package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.TransPlanInfo;
import com.example.yjyt.domain.YardInfo;
import com.example.yjyt.mapper.TransPlanMapper;
import com.example.yjyt.mapper.YardMapper;
import com.example.yjyt.serv.TransPlanInfoServ;
import com.example.yjyt.serv.YardInfoServ;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TransPlanInfoServImpl extends ServiceImpl<TransPlanMapper, TransPlanInfo> implements TransPlanInfoServ {
    @Autowired
    private TransPlanMapper transPlanMapper;

    
}
