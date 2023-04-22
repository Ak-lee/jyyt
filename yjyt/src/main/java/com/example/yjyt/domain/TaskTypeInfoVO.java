package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;
import java.sql.Date;
import java.util.List;

@Data
@TableName("tasktype_info")
// 检修任务类型信息+耗费模式list
public class TaskTypeInfoVO extends TaskTypeInfo implements Serializable {
    public List<TaskTypeInfoVO> list;
}
