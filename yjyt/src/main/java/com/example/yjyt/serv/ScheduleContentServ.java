package com.example.yjyt.serv;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.yjyt.domain.ScheduleContent;
import com.example.yjyt.domain.ScheduleContentVO;

import java.util.List;

public interface ScheduleContentServ extends IService<ScheduleContent> {
    List<ScheduleContentVO> getContentByScheduleId(String scheduleId);

    List<ScheduleContentVO> getContentBylineId(Integer lineId);

}
