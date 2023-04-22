package com.example.yjyt.serv;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.example.yjyt.domain.OnedayMaxInfo;
import com.example.yjyt.domain.OnedayMaxInfoVO;
import com.example.yjyt.domain.ScheduleInfoVO;

public interface OnedayMaxServ extends IService<OnedayMaxInfo> {
    void getPageByLineId(Page<OnedayMaxInfoVO> page, Integer lineId);
}
