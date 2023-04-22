package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * @TableName yard_shop_tasktypes_mapper
 */
@TableName(value ="yard_shop_tasktypes_mapper")
@Data
public class YardShopTasktypes implements Serializable {
    @TableId(type = IdType.ASSIGN_ID)
    private Long id;

    private String yardId;

    private Long tasktypeId;

    private String shopNameString;    // 检修库、运用库 或者 “检修库,运用库”

    private static final long serialVersionUID = 1L;
}