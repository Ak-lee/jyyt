package com.example.yjyt.serv;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.example.yjyt.domain.TrainInfo;
import com.example.yjyt.domain.TrainInfoVO;

public interface TrainInfoServ extends IService<TrainInfo> {
    void getPageByLineId(Page<TrainInfoVO> page, Integer lineId);

    void getPage(Page<TrainInfoVO> page);
}
