package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * @TableName hot_backup_train_num
 */
@TableName(value ="hot_backup_train_num")
@Data
public class HotBackupTrainNum implements Serializable {
    private Long id;

    private Integer lineId;

    private String applicableTime;

    private Integer hotBackupTrainNum;

    private static final long serialVersionUID = 1L;
}