package com.example.yjyt.util;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.Date;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

@Getter
@Setter
@ToString
public class DateRange {
    private Date startDate;
    private Date endDate;

    public DateRange(Date start, Date end) {
        startDate = start;
        endDate = end;
    }

    public List<Date> subRange(DateRange range) {
        List<Date> dateList1;
        dateList1 = findDates(startDate, endDate);

        List<Date> dateList2;
        dateList2 = findDates(range.getStartDate(), range.getEndDate());

        dateList1.removeAll(dateList2);
        return dateList1;
    }

    public static List<Date> findDates(Date dBegin, Date dEnd) {
        List lDate = new ArrayList();
        lDate.add(dBegin);
        Calendar calBegin = Calendar.getInstance();
// 使用给定的 Date 设置此 Calendar 的时间
        calBegin.setTime(dBegin);
        Calendar calEnd = Calendar.getInstance();
// 使用给定的 Date 设置此 Calendar 的时间
        calEnd.setTime(dEnd);
// 测试此日期是否在指定日期之后
        while (dEnd.after(calBegin.getTime())) {
// 根据日历的规则，为给定的日历字段添加或减去指定的时间量
            calBegin.add(Calendar.DAY_OF_MONTH, 1);
            lDate.add(calBegin.getTime());
        }
        return lDate;
    }
}
