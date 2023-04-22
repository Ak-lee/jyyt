package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * @TableName operation plan
 */
@TableName(value ="operation_plan")
@Data
public class OperationPlan implements Serializable {
    private Long id;

    private String pingfengTask;

    private String hotBackupTask;

    private String cannotForPeakTask;

    private String dayScheduleId;

    private Integer lineId;

    private static final long serialVersionUID = 1L;
}