package com.example.yjyt.permission;

import com.google.common.collect.Sets;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class CacheManager {

    // 保存用户和具有的角色之间的对应关系
    public static final Map<String, Set<String>> USER_ROLE_MAP = new HashMap<>();

    static {
        // 用户张三具有 user 和 admin 两个角色
        Set<String> roleSet3 = Sets.newHashSet("admin", "user");
        USER_ROLE_MAP.put("zhangsan", roleSet3);

        // 用户 lisi 具有 user 一个角色
        Set<String> roleSet4 = Sets.newHashSet("user");
        USER_ROLE_MAP.put("lisi", roleSet4);
    }
}
