package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.LineYardInfo;
import com.example.yjyt.domain.YardInfo;
import com.example.yjyt.mapper.LineYardMapper;
import com.example.yjyt.mapper.YardMapper;
import com.example.yjyt.serv.LineYardInfoServ;
import com.example.yjyt.serv.YardInfoServ;
import org.springframework.stereotype.Service;

@Service
public class LineYardInfoServImpl extends ServiceImpl<LineYardMapper, LineYardInfo> implements LineYardInfoServ {
}
