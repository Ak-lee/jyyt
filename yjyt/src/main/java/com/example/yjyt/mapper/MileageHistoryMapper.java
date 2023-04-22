package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.MileageHistory;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.Date;
import java.util.List;
import java.util.Map;

@Mapper
public interface MileageHistoryMapper extends BaseMapper<MileageHistory> {
    @Select("select * from mileage_history mh " +
            "left join train_info ti on mh.train_id = ti.id " +
            "where ti.line_id = #{lineId} and " +
            "mh.date between #{sdate} and #{edate} "
    )
    List<MileageHistory> getMileageList(Integer lineId, Date sdate, Date edate);

    @Select("select Min(date) min_date, Max(date) max_date from mileage_history mh " +
            "left join train_info ti on mh.train_id = ti.id " +
            "where ti.line_id = #{lineId} ")
    public Map<String, Date> getPagesOverview(Integer lineId);
}

