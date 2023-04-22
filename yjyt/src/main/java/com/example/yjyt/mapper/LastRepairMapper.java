package com.example.yjyt.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.yjyt.domain.LastRepairInfo;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LastRepairMapper extends BaseMapper<LastRepairInfo> {

}
