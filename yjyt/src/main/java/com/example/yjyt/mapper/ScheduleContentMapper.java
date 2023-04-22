
package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.ScheduleContent;
import com.example.yjyt.domain.ScheduleContentVO;
import com.example.yjyt.domain.ScheduleInfoVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.sql.Date;
import java.util.List;


@Repository
public interface ScheduleContentMapper extends BaseMapper<ScheduleContent> {
    @Select("select sc.*, si.plan_type as plan_type, si.dispatch_status as dispatch_status\n" +
            "from schedule_content sc\n" +
            "left join schedule_info si on sc.schedule_id = si.id\n" +
            "where sc.schedule_id = #{scheduleId}")
    public List<ScheduleContentVO> getContent(@Param("scheduleId") String scheduleId);

    @Select("select sc.*, si.plan_type as plan_type, si.dispatch_status as dispatch_status\n" +
            "from schedule_content sc\n" +
            "left join schedule_info si on sc.schedule_id = si.id\n" +
            "where si.line_id = #{lineId}")
    public List<ScheduleContentVO> getContentAll(@Param("lineId") Integer lineId);

    @Select("select * from schedule_content where plan_date < #{content.planDate} " +
            "and task_type = #{content.taskType} and train_id = #{content.trainId} " +
            "order by plan_date desc limit 1")
    public ScheduleContent getLastTask(@Param("content") ScheduleContent content);

    @Select("select * from schedule_content where plan_date > #{content.planDate} " +
            "and task_type = #{content.taskType} and train_id = #{content.trainId} " +
            "order by plan_date limit 1")
    public ScheduleContent getNextTask(@Param("content") ScheduleContent content);

    @Select("select * from schedule_content where plan_date > #{planDate} " +
            "and task_type = #{taskType} and train_id = #{trainId} " +
            "order by plan_date limit 1")
    public ScheduleContent getNextTaskItem(Date planDate, String taskType, String trainId);

    @Select("SELECT r.id, l.train_id, l.plan_date, r.schedule_id, r.duration, r.task_type, r.task_content FROM " +
            "( SELECT train_id, Max( plan_date ) plan_date FROM schedule_content WHERE (task_type = '均衡修' || task_type='季节检' || task_type='大修' || task_type='架修') " +
            " AND plan_date < #{deadline} AND schedule_id = #{scheduleId} " +
            "GROUP BY train_id ) l " +
            "LEFT JOIN ( SELECT * FROM schedule_content  WHERE task_type = '均衡修' || task_type='季节检' || task_type='大修' || task_type='架修') r ON l.train_id = r.train_id " +
            "AND l.plan_date = r.plan_date")
    public List<ScheduleContent> getLastRepairType(String scheduleId, Date deadline);

    @Select("select schedule_content.*, train_info.line_id from schedule_content left join train_info\n" +
            "on train_info.id = schedule_content.train_id\n" +
            "where train_info.line_id = #{lineId}} and\n" +
            "schedule_content.task_type = '均衡修' || schedule_content.task_type='季节检' || schedule_content.task_type='大修' || schedule_content.task_type='架修'\n" +
            "and schedule_content.plan_date < #{deadline}")
    public List<ScheduleContent> getLastRepairType(Integer lineId, Date deadline);


    @Select("select * from schedule_content where schedule_id=#{scheduleId} and plan_date between #{start} and #{end}")
    public List<ScheduleContent> listByScheduleIdAndRange(String scheduleId, Date start, Date end);

    @Select("select sc.*, si.plan_type as plan_type, si.dispatch_status as dispatch_status\n" +
            "from schedule_content sc\n" +
            "left join schedule_info si on sc.schedule_id = si.id\n" +
            "where si.line_id = #{lineId} and sc.plan_date between #{start} and #{end}")
    public List<ScheduleContent> listByRangeAndLineId(Integer lineId, Date start, Date end);

    @Select("select schedule_content.*, schedule_info.plan_type from schedule_content \n" +
            "left join schedule_info on schedule_content.schedule_id = schedule_info.id \n" +
            "where #{date} between plan_date \n" +
            "and adddate(plan_date, interval duration - 1 day) \n" +
            "and schedule_info.line_id = #{lineId}")
    public List<ScheduleContentVO> listByLineIdAndDate(Integer lineId, Date date);
}
