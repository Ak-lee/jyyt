package com.example.yjyt.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * @TableName forcast_picture
 */
@TableName(value ="forcast_picture")
@Data
public class ForcastPicture implements Serializable {
    private String trainId;

    private byte[] picture;

    private static final long serialVersionUID = 1L;
}