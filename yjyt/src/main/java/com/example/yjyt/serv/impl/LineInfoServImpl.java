package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.LineInfo;
import com.example.yjyt.domain.LineInfoVO;
import com.example.yjyt.exception.BusinessException;
import com.example.yjyt.mapper.LineMapper;
import com.example.yjyt.serv.LineInfoServ;
import org.springframework.stereotype.Service;

@Service
public class LineInfoServImpl extends ServiceImpl<LineMapper, LineInfo> implements LineInfoServ {
    public Page<LineInfoVO> getPage(Page<LineInfoVO> page, String key) {
        if (key != null) {
            key = '%' + key + '%';
        }
        return baseMapper.getPage(page, key);
    }

    public LineInfoVO getByLineId(Integer lineId) {
        return baseMapper.getByLineId(lineId);
    }

    public boolean save(LineInfo lineInfo) {
        LineInfo item = baseMapper.selectById(lineInfo.getId());
        if (item == null) {
            baseMapper.insert(lineInfo);
            return true;
        } else {
            throw new BusinessException("id 已存在");
        }
    }
}
