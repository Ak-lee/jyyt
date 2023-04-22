package com.example.yjyt.serv;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.example.yjyt.domain.Station;
import com.example.yjyt.domain.StationVO;

public interface StationServ extends IService<Station> {
    void getPageByLineId(Page<StationVO> page, Integer lineId);

    void getPage(Page<StationVO> page);
}
