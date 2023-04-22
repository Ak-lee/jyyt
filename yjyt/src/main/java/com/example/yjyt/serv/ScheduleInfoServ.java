
package com.example.yjyt.serv;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.example.yjyt.domain.ScheduleInfo;
import com.example.yjyt.domain.ScheduleInfoVO;

public interface ScheduleInfoServ  extends IService<ScheduleInfo> {
    void getPageByLineId(Page<ScheduleInfoVO> page, String planType, Integer lineId);
}
