package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import java.util.Date;
import lombok.Data;

/**
 * @TableName day_plan_history
 */
@TableName(value ="day_plan_history")
@Data
public class DayPlanHistory implements Serializable {
    private Long id;

    private Date date;

    private String trainId;

    private Integer lineId;

    private Integer lastUndercarId;

    private String workYard;

    private String backYard;

    private static final long serialVersionUID = 1L;
}