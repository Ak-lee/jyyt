package com.example.yjyt.serv.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.domain.YardInfo;
import com.example.yjyt.domain.YardShopTasktypes;
import com.example.yjyt.domain.YardTaskTypeListVO;
import com.example.yjyt.exception.BusinessException;
import com.example.yjyt.serv.YardShopTasktypesMapperService;
import com.example.yjyt.mapper.YardShopTasktypesMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;
import java.util.Objects;

/**
 * @author 29547
 * @description 针对表【yard_shop_tasktypes_mapper(yard_shop_tasktypes_mapper
 * 进行车场的车库（检修库、运用库）、检修任务类型的关联表。)】的数据库操作Service实现
 * @createDate 2023-03-03 10:39:13
 */
@Service
public class YardShopTasktypesMapperServiceImpl extends ServiceImpl<YardShopTasktypesMapper, YardShopTasktypes>
        implements YardShopTasktypesMapperService {

    @Autowired
    private YardInfoServImpl serv2;

    @Autowired
    YardTasktypeMapperServiceImpl serv3;

    public int saveItem(YardShopTasktypes item) {
        // 根据车场的适用检修任务类型，存储该检修任务类型能在哪些地点（检修库、运用库）维修
        YardInfo yard = serv2.getById(item.getYardId());
        if (!yard.isBeDepot()) {// 判断是否为车辆段
            // 若不是车辆段
            throw new BusinessException("该车场不是车辆段, 保存失败.");
        } else {
            YardTaskTypeListVO temp = serv3.getListVOByYardIdAndTaskTypeId(item.getYardId(), item.getTasktypeId());
            if (temp == null) {
                throw new BusinessException("保存失败,车场不支持该检修任务类型");
            } else {
                // 存储检修库、运用库
                List<String> list = Arrays.asList(item.getShopNameString().split(","));
                list.forEach(j -> {
                    if (!Objects.equals(j, "检修库") && !Objects.equals(j, "运用库")) {
                        throw new BusinessException("保存失败,检修地点字段错误");
                    }
                    if (j.equals("检修库") && !yard.isHasServiceShop()) {
                        throw new BusinessException("保存失败，该车场无检修库");
                    }
                    if (j.equals("运用库") && !yard.isHasOperationShop()) {
                        throw new BusinessException("保存失败，该车场无运用库");
                    }
                });
                return baseMapper.insert(item);
            }
        }
    }
}