package com.example.yjyt.ResultHandler;

import com.example.yjyt.domain.ScheduleContentHistory;
import com.example.yjyt.domain.ScheduleContentHistoryBeforeSync;
import com.example.yjyt.serv.impl.ScheduleContentHistoryImpl;
import org.apache.ibatis.session.ResultContext;
import org.apache.ibatis.session.ResultHandler;

import java.sql.Date;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ScheduleContentHistoryHandler
        implements ResultHandler<ScheduleContentHistoryBeforeSync> {
    private ScheduleContentHistoryImpl serv;

    // 这是每批处理的大小
    private final static int BATCH_SIZE = 1000;
    private int size;
    // 存储每批数据的临时容器
    private Set<ScheduleContentHistoryBeforeSync> set;
    private Set<ScheduleContentHistory> set2;

    public void handleResult(ResultContext<? extends ScheduleContentHistoryBeforeSync> resultContext) {
        // 这里获取流式查询每次返回的单条结果
        ScheduleContentHistoryBeforeSync item = resultContext.getResultObject();
        // 你可以看自己的项目需要分批进行处理或者单个处理，这里以分批处理为例
        set.add(item);
        size++;
        if (size == BATCH_SIZE) {
            handle();
        }
    }

    private void handle() {
        try {
            // 在这里可以对你获取到的批量结果数据进行需要的业务处理
            set.forEach(i -> {
                // 如 SFM64-均衡修4B-2-17009
                // 如 SFM64-里程检无电、有电、车顶-1-17006
                // 如 SFM64-季节专检10-1-CD17003
                // 如 SFM64-里程检车顶-2-17015-12月30日9:00-17:00， 即登顶检
                String overhaulPlanName = i.getOverhaulPlanName();
                String trainId = i.getOverhaulTrainName();
                Date planStartDate = i.getPlanStartDate();
                Date planEndDate = i.getPlanEndDate();
                Integer duration = (int) ((planEndDate.getTime() - planStartDate.getTime()) / (1000 * 3600 * 24));

                ScheduleContentHistory item = new ScheduleContentHistory();
                item.setPerformDate(planStartDate);
                item.setDuration(duration);
                item.setTrainId(trainId);
                String[] split = overhaulPlanName.split("-");
                List<String> list = Arrays.asList(split);

                System.out.println(list);

                if (list.get(1).contains("均衡修")) {
                    String regEx = "[^0-9]";
                    Pattern p = Pattern.compile(regEx);
                    Matcher m = p.matcher(list.get(1));

                    String month = m.replaceAll("").trim();
                    String content = list.get(1).substring(list.get(1).indexOf(month));
                    content = content + list.get(2) + "Y";
                    item.setApplyMonth(Integer.valueOf(month));
                    item.setTaskType("均衡修");
                    item.setTaskContent(content);
                } else if (list.get(1).contains("季节专检")) {
                    item.setTaskType("均衡修");
                } else if (list.get(1).contains("里程检车顶")) {
                    item.setTaskType("登顶检");
                } else if (list.get(1).contains("里程检")) {
                    item.setTaskType("里程检");
                }
                set2.add(item);
            });
        } finally {
            // 处理完每批数据后后将临时清空
            serv.saveBatch(set2);
            set2.clear();
            size = 0;
            set.clear();
        }
    }

    // 这个方法给外面调用，用来完成最后一批数据处理
    public void end() {
        handle();// 处理最后一批不到BATCH_SIZE的数据
    }


}
