package com.example.yjyt.domain.excel;

import com.alibaba.excel.annotation.ExcelProperty;
import com.alibaba.excel.annotation.format.DateTimeFormat;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.sql.Date;
import java.util.Objects;

@Getter
@Setter
@EqualsAndHashCode
@ToString
public class UploadData {
    private String trainId;
    private Integer mileage;
    @DateTimeFormat("yyyy-MM-dd")
    private Date date;
    private Integer id;

    @Override
    // 只要列车号和日期相同，即认为相同的对象，忽略了里程的差别
    // 当然这里只适用于excel多行数据直接的判重，不适用于excel中的数据和数据库中的数据判重
    public boolean equals(Object o) {
        if (o == null || !(o instanceof UploadData)) {
            return false;
        } else {
            return this.getTrainId().equals(((UploadData) o).getTrainId())
                    && this.getDate().equals(((UploadData) o).getDate());
        }
    }

    @Override
    public int hashCode() {
        return Objects.hash(trainId, date);
    }

}
