package com.example.yjyt.codeinfo.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.codeinfo.domain.CodeInfo;
import com.example.yjyt.codeinfo.domain.dto.CodeDTO;
import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface CodeInfoDao extends BaseMapper<CodeInfo> {

    @Select("select ifnull(MAX(seq),0) from sys_code_info")
    Integer getMaxSeq();

    @Update("update sys_code_info set status = 2 where id = #{id} ")
    void stopById(@Param("id") String id);

    @Update("update sys_code_info set status = 1 where id = #{id} ")
    void startById(@Param("id") String id);

    @Select("select * from sys_code_info where id = #{id}")
    CodeInfo findById(@Param("id") String id);

    @Insert("insert into sys_code_info(id, name, expression, status, seq,flowNum,className) value (#{id} ,#{name} ,#{expression} ,#{status} ,#{seq},#{flowNum},#{className})")
    void save(CodeInfo codeInfo);

    @Select("select * from sys_code_info t order by t.seq")
    List<CodeInfo> listPage();

    @Delete("delete from sys_code_info where id = #{id}")
    void deleteById(@Param("id") String id);

    @Select("select * from sys_code_info where className = #{className} and status = 1")
    CodeInfo findByClassName(@Param("className") String className);

    @Update("update sys_code_info set name = #{name} , expression = #{expression} where id = #{id}")
    void update(CodeDTO dto);

    @Update("update sys_code_info set flowNum = #{flowNum} + 1  where id = #{id}")
    void nextFlow(CodeInfo code);

    @Update("update sys_code_info set status = 1  where id = #{id}")
    void enable(@Param("id") String id);

    @Update("update sys_code_info set status = 2  where id = #{id}")
    void disable(@Param("id") String id);

    @Select("select * from sys_code_info where name = #{name} limit 1")
    CodeInfo findByCodeName(@Param("name") String name);

    @Select("select * from sys_code_info where status = 1")
    List<CodeInfo> list();

    @Update("update sys_code_info set flowNum = #{flowNum} + #{count}  where id = #{id}")
    void updateFlow(@Param("id") String id, @Param("flowNum") Integer flowNum, @Param("count") long count);
}
