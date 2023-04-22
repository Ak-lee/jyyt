package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.OnedayMaxInfo;
import com.example.yjyt.domain.OnedayMaxInfoVO;
import com.example.yjyt.mapper.OnedayMaxMapper;
import com.example.yjyt.serv.OnedayMaxServ;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class OnedayMaxServImpl extends ServiceImpl<OnedayMaxMapper, OnedayMaxInfo> implements OnedayMaxServ {
//    @Autowired
//    private OnedayMaxMapper onedayMaxMapper;
    @Override
    public void getPageByLineId(Page<OnedayMaxInfoVO> page, Integer lineId) {
        baseMapper.getPage(page, lineId);
    }

    public void getPage(Page<OnedayMaxInfoVO> page) {
        baseMapper.getPageAll(page);
    }

    public List<OnedayMaxInfo> getAllByLineId(Integer lineId) {
        QueryWrapper<OnedayMaxInfo> wrapper = new QueryWrapper<>();
        wrapper.eq("line_id", lineId);
        List<OnedayMaxInfo> list = baseMapper.selectList(wrapper);
        return list;
    }
}
