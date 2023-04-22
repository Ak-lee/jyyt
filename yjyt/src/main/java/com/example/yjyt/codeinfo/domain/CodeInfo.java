package com.example.yjyt.codeinfo.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Getter;
import lombok.Setter;


@Getter
@Setter
@TableName("sys_code_info")
public class CodeInfo {
	private static final long serialVersionUID = 1L;

	@TableId(type = IdType.ASSIGN_ID)
	private String id;
	private String name;
	private String expression;
	private Integer status;
	private Integer seq;
	private Integer flowNum;
	private String previewText;
	private String className;
	private String classType;
}
