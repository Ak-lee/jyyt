package com.example.yjyt.mapper;

import com.example.yjyt.common.R;
import com.example.yjyt.domain.ScheduleContent;
import com.example.yjyt.domain.ScheduleContentHistory;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.ScheduleContentHistoryVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.sql.Date;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public interface ScheduleContentHistoryMapper extends BaseMapper<ScheduleContentHistory> {

    @Select({
            "<script> ",
            "select sch.*, si.plan_type as plan_type ",
            "from schedule_content_history sch ",
            "left join schedule_info si on sch.schedule_id = si.id ",
            "where si.line_id = #{lineId}",
            "<if test='planTypes != null'>",
            "and si.plan_type in <foreach item='item' index='index' collection='planTypes' open='(' separator=',' close=')'>#{item}</foreach> ",
            "</if>",
            "<if test='sdate != null and edate != null'>",
            "and sch.perform_date between #{sdate} and #{edate} ",
            "</if>",
            "<if test='status != null'>",
            "and sch.status = #{status} ",
            "</if>",
            "</script> "
    })
    public List<ScheduleContentHistoryVO> tableWithCond(Integer lineId, List<String> planTypes, Date sdate, Date edate, String status);

    @Select({
            "<script> ",
            "select count(*) count, Min(perform_date) start_date from schedule_content_history sch ",
            "left join schedule_info si on sch.schedule_id = si.id ",
            "where si.line_id = #{lineId} ",
            "<if test='planTypes != null'> ",
            "and si.plan_type in <foreach item='item' index='index' collection='planTypes' open='(' separator=',' close=')'>#{item}</foreach> ",
            "</if> ",
            "</script>"
    })
    public Map<String, Object> getPagesOverview(Integer lineId, List<String> planTypes);

    @Select("select sch.*, si.plan_type as plan_type , si.dispatch_status as dispatch_status " +
            "from schedule_content_history sch " +
            "left join schedule_info si on sch.schedule_id = si.id " +
            "where sch.schedule_id = #{scheduleId}")
    public List<ScheduleContentHistoryVO> getContent(@Param("scheduleId") String scheduleId);

    @Select("select sch.*, si.plan_type as plan_type , si.dispatch_status as dispatch_status " +
            "from schedule_content_history sch " +
            "left join schedule_info si on sch.schedule_id = si.id")
    public List<ScheduleContentHistoryVO> getAllContent();

//    @Select("SELECT r.id, l.train_id, l.perform_date, r.schedule_id, r.duration, r.task_type, r.task_content, r.status FROM " +
//            "( SELECT train_id, Max( perform_date ) perform_date FROM schedule_content_history " +
//            "WHERE (task_type = '均衡修' || task_type='季节检' || task_type='大修' || task_type='架修') AND perform_date < #{deadline} " +
//            "AND schedule_id = #{scheduleId} " +
//            "AND task_content rlike #{monthStr} " +
//            "GROUP BY train_id ) l " +
//            "LEFT JOIN (select * from schedule_content_history where task_type = '均衡修' || task_type='季节检' || task_type='大修' || task_type='架修') r ON l.train_id = r.train_id " +
//            "AND l.perform_date = r.perform_date")
//    public List<ScheduleContentHistory> getLastRepairMode(@Param("scheduleId") String scheduleId, Date deadline, String monthStr);

    @Select("SELECT r.id, l.train_id, l.perform_date, r.schedule_id, r.duration, r.task_type, r.task_content, r.status FROM " +
            "( SELECT train_id, Max( perform_date ) perform_date FROM schedule_content_history " +
            "WHERE (task_type = '均衡修' || task_type='季节检' || task_type='大修' || task_type='架修') AND perform_date < #{deadline} " +
            "AND schedule_id = #{scheduleId} " +
            "AND apply_month = #{month} " +
            "GROUP BY train_id ) l " +
            "LEFT JOIN (select * from schedule_content_history where task_type = '均衡修' || task_type='季节检' || task_type='大修' || task_type='架修') r ON l.train_id = r.train_id " +
            "AND l.perform_date = r.perform_date")
    public List<ScheduleContentHistory> getLastRepairMode(@Param("scheduleId") String scheduleId, Date deadline, Integer month);

//    @Select("select schedule_content_history.*, train_info.line_id from schedule_content_history " +
//            "left join train_info\n" +
//            "on train_info.id = schedule_content_history.train_id\n" +
//            "where train_info.line_id = #{lineId} and\n" +
//            "schedule_content_history.task_type = '均衡修' || schedule_content_history.task_type='季节检' " +
//            "|| schedule_content_history.task_type='大修' || schedule_content_history.task_type='架修'\n" +
//            "and schedule_content_history.perform_date < #{deadline} " +
//            "AND schedule_content_history.task_content rlike #{monthStr} ")
//    public List<ScheduleContentHistory> getLastRepairMode2(Integer lineId, Date deadline, String monthStr);

    @Select("select schedule_content_history.*, train_info.line_id from schedule_content_history " +
            "left join train_info\n" +
            "on train_info.id = schedule_content_history.train_id\n" +
            "where train_info.line_id = #{lineId} and\n" +
            "schedule_content_history.task_type = '均衡修' || schedule_content_history.task_type='季节检' " +
            "|| schedule_content_history.task_type='大修' || schedule_content_history.task_type='架修'\n" +
            "and schedule_content_history.perform_date < #{deadline} " +
            "AND schedule_content_history.apply_month = #{month} ")
    public List<ScheduleContentHistory> getLastRepairMode2(Integer lineId, Date deadline, Integer month);

    @Select("SELECT r.id, l.train_id, l.perform_date, r.schedule_id, r.duration, r.task_type, r.task_content FROM " +
            "( SELECT train_id, Max( perform_date ) perform_date FROM schedule_content_history WHERE (task_type = '均衡修' || task_type='季节检' || task_type='大修' || task_type='架修') " +
            " AND perform_date < #{deadline} AND schedule_id = #{scheduleId} " +
            "GROUP BY train_id ) l " +
            "LEFT JOIN ( SELECT * FROM schedule_content_history  WHERE task_type = '均衡修' || task_type='季节检' || task_type='大修' || task_type='架修') r ON l.train_id = r.train_id " +
            "AND l.perform_date = r.perform_date")
    public List<ScheduleContentHistory> getLastRepairType(@Param("scheduleId") String scheduleId, Date deadline);

    @Select("SELECT \tr.id,\tl.train_id,\tl.perform_date,\tr.schedule_id,\n" +
            "\tr.duration,\tr.task_type,\tr.task_content,\tr.STATUS \n" +
            "FROM\t(\n" +
            "\tSELECT train_id, Max( perform_date ) perform_date \n" +
            "\tFROM \t\tschedule_content_history \n" +
            "\tWHERE \n" +
            "\t\t( task_type = '均衡修' || task_type = '季节检' || task_type = '大修' || task_type = '架修' ) \n" +
            "\t\tAND perform_date < #{deadline} \n" +
            "\t\tGROUP BY train_id \n" +
            "\t) l\n" +
            "\tLEFT JOIN ( SELECT * FROM schedule_content_history WHERE task_type = '均衡修' || task_type = '季节检' || task_type = '大修' || task_type = '架修' ) r ON l.train_id = r.train_id \tAND l.perform_date = r.perform_date\n" +
            "\tLEFT JOIN train_info ON train_info.id = r.train_id\n" +
            "\twhere train_info.line_id = #{lineId}")
    public List<ScheduleContentHistory> getLastRepairType2(Integer lineId, Date deadline);

    @Select("SELECT r.id, l.train_id, l.perform_date, r.schedule_id, r.duration, r.task_type, r.task_content FROM " +
            "( SELECT train_id, Max( perform_date ) perform_date FROM schedule_content_history WHERE (task_type = '登顶检') " +
            " AND perform_date < #{deadline} AND schedule_id = #{scheduleId} " +
            "GROUP BY train_id ) l " +
            "LEFT JOIN ( SELECT * FROM schedule_content_history WHERE task_type = '登顶检') r ON l.train_id = r.train_id " +
            "AND l.perform_date = r.perform_date")
    // 根据传入的月计划 Id
    public List<ScheduleContentHistory> getLatestMonthRepairType(@Param("scheduleId") String scheduleId, Date deadline);

    @Select("SELECT r.id, l.train_id, l.perform_date, r.schedule_id, r.duration, r.task_type, r.task_content FROM " +
            "( SELECT train_id, Max( perform_date ) perform_date FROM schedule_content_history WHERE (task_type = '登顶检') " +
            " AND perform_date < #{deadline} AND line_id = #{lineId} " +
            "GROUP BY train_id ) l " +
            "LEFT JOIN ( SELECT * FROM schedule_content_history WHERE task_type = '登顶检') r ON l.train_id = r.train_id " +
            "AND l.perform_date = r.perform_date")
    public List<ScheduleContentHistory> getLatestMonthRepairType2(Integer lineId, Date deadline);


    @Select("select * from schedule_content_history where task_type = '登顶检' order by perform_date desc limit 1")
    public ScheduleContentHistory getLatestMonth(); // 获取历史记录中的最近一条月计划登顶检

    @Select("SELECT r.id, l.train_id, l.perform_date, r.schedule_id, r.duration, r.task_type, r.task_content FROM " +
            "( SELECT train_id, Max( perform_date ) perform_date FROM schedule_content_history WHERE (task_type = '里程检') " +
            " AND perform_date < #{deadline} AND schedule_id = #{scheduleId} " +
            "GROUP BY train_id ) l " +
            "LEFT JOIN ( SELECT * FROM schedule_content_history WHERE task_type = '里程检') r ON l.train_id = r.train_id " +
            "AND l.perform_date = r.perform_date")
    // 根据传入的周计划 Id
    public List<ScheduleContentHistory> getLatestWeekRepairType(@Param("scheduleId") String scheduleId, Date deadline);

    @Select("SELECT r.id, l.train_id, l.perform_date, r.schedule_id, r.duration, r.task_type, r.task_content FROM " +
            "( SELECT train_id, Max( perform_date ) perform_date FROM schedule_content_history WHERE (task_type = '里程检') " +
            " AND perform_date < #{deadline} AND line_id = #{lineId} " +
            "GROUP BY train_id ) l " +
            "LEFT JOIN ( SELECT * FROM schedule_content_history WHERE task_type = '里程检') r ON l.train_id = r.train_id " +
            "AND l.perform_date = r.perform_date")
    public List<ScheduleContentHistory> getLatestWeekRepairType2(Integer lineId, Date deadline);

    @Select("SELECT\n" +
            "\tr.* \n" +
            "FROM\n" +
            "\t( SELECT train_id, Max( perform_date ) perform_date FROM schedule_content_history " +
            "WHERE perform_date < #{deadline} AND line_id = #{lineId} GROUP BY train_id ) l\n" +
            "\tLEFT JOIN ( SELECT * FROM schedule_content_history ) r ON l.train_id = r.train_id \n" +
            "\tAND l.perform_date = r.perform_date")
    public List<ScheduleContentHistory> lastAnyTypeRepairByLineId(Integer lineId, Date deadline);

    @Select("select * from schedule_content_history where task_type = '里程检' order by perform_date desc limit 1")
    public ScheduleContentHistory getLatestWeek(); // 获取历史记录中的最近一条周计划登顶检

    @Select({
            "<script> ",
            "select *\n",
            "from \n",
            "(select max(perform_date) l_date, train_id l_train from schedule_content_history\n",
            "where line_id=#{lineId} ",
            "and apply_month=#{month} ",
            "and perform_date &lt; #{deadline} and task_type = #{tasktypeName} \n",
            "GROUP BY train_id\n",
            ") l\n",
            "left join (\n",
            "select * from schedule_content_history ",
            "where line_id=#{lineId} ",
            "and apply_month=#{month} ",
            "and perform_date &lt; #{deadline} ",
            "and task_type = #{tasktypeName} \n",
            ") r on r.perform_date =l_date and r.train_id = l_train",
            "</script>"
    })
    public List<ScheduleContentHistory> filterByLineIdMonthTaskTypeNameDeadline(
            Integer lineId, Integer month, String tasktypeName, Date deadline
    );

}




