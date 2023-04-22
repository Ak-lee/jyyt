
package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.TeamInfo;
import com.example.yjyt.mapper.TeamMapper;
import com.example.yjyt.serv.TeamInfoServ;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TeamInfoServImpl extends ServiceImpl<TeamMapper, TeamInfo> implements TeamInfoServ {
    public List<TeamInfo> getAll() {
        return baseMapper.selectList(null);
    }

}
