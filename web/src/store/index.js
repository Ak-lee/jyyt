import {createStore} from 'vuex'

export default createStore({
    state: {
        // state 中定义全局共享数据
        menuStruct: [       // 规定，先渲染有3级菜单的条目，后渲染有2级菜单的条目
            {
                "name": "里程预测管理",
                "path": "/mileage-predict",
                "child": [
                    {
                        "name": "历史数据导入",
                        "path": "/history-data-import",
                        "child": []
                    },
                    {
                        "name": "模型预测结果",
                        "path": "/predict-res",
                        "child": [],
                    },
                ]
            },
            {
                "name": "线路资源管理",
                "path": "/line",
                "child": [
                    {
                        "name": "线路基本信息",
                        "path": "/basicInfo",
                        "child": []
                    },
                    {
                        "name": "线路详情信息",
                        "path": "/lineDetail",
                        "child": []
                    },
                    {
                        "name": "线路站点信息管理",
                        "path": "/stationInfo",
                        "child": []
                    },
                    {
                        "name": "列车信息管理",
                        "path": "/trainInfo",
                        "child": []
                    },
                    {
                        "name": "生产日历信息管理",
                        "path": "/calendar",
                        "child": [],
                    },
                    {
                        "name": "线路配属车场管理",
                        "path": "/yard",
                        "child": [
                            {
                                "name": "车库基本信息",
                                "path": "/yard-info",
                            },
                            {
                                "name": "车库详情信息",
                                "path": "/yard-detail",
                            },
                        ]
                    },
                    {
                        "name": "检修任务管理",
                        "path": "/overhaul",
                        "child": [
                            {
                                "name": "检修任务类型基础信息",
                                "path": "/type"
                            },
                            {
                                "name": "检修任务类型详情信息",
                                "path": "/typeDetail"
                            },
                            {
                                "name": "线路检修约束管理",
                                "path": "/constraint"
                            },
                            {
                                "name": "历史检修数据管理",
                                "path": "/historyRepairs"
                            }
                        ]
                    },
                    {
                        "name": "检修班组管理",
                        "path": "/team",
                        "child": [
                            {
                                "name": "人员技能管理",
                                "path": "/skill"
                            }
                        ]
                    },
                ]
            },
            {
                "name": "计划制定管理",
                "path": "/task",
                "child": [
                    {
                        "name": "运输任务管理",
                        "path": "/transPlan",
                        "child": []
                    },
                    {
                        "name": "计划任务管理",
                        "path": "/plan",
                        "child": [
                            {
                                "name": "计划类型和检修任务的对应关系",
                                "path": "/relation"
                            },
                            {
                                "name": "年计划信息管理",
                                "path": "/year"
                            },
                            {
                                "name": "月计划信息管理",
                                "path": "/month"
                            },
                            {
                                "name": "周计划信息管理",
                                "path": "/week"
                            },
                            {
                                "name": "日计划信息管理",
                                "path": "/day"
                            },
                            {
                                "name": "执行计划查询与下发",
                                "path": "/planInquiry"
                            },
                            {
                                "name": "历史检修计划查询",
                                "path": "/historyPlanQuery"
                            },
                            {
                                "name": "计划反馈",
                                "path": "/planFeedback"
                            },
                        ]
                    },
                ]
            },

        ],
        menu1Index: "0", // 目前选中的是一级标题中的第几个，从 0 开始计数,
        lineId: "",
        trainId: "",
        leftNavFold: false,
        // item : {trainId: '', date: '', mileage: '', prevMileage: '', type: ''}
        mileageChangeInsideTable: [],
        mileageChangeOutsideTable: [],
        addItem(arr, item) {
            if (item.date && item.trainId && item.mileage && item.type) {
                let index = arr.findIndex(i => {
                    return i.trainId === item.trainId && i.date === item.date
                })
                if (index === -1) {
                    arr.push(item)
                } else {
                    arr[index] = item;
                }
            }
        },
        removeItem(arr, item) {
            if (item.date && item.trainId && item.mileage) {
                // 若这些属性都存在的话
                let index = arr.findIndex(i => {
                    return i.trainId == item.trainId && i.date == item.date
                })
                if (index === -1) {
                    return;
                } else {
                    arr.splice(index, 1);
                }
            }
        },
    },
    getters: {
        // 返回一级标题名
        menuNames: (state) => {
            let menu = []
            state.menuStruct.forEach((item) => {
                menu.push(item.name)
            })
            return menu
        },
        getMenu2: (state) => {
            // 返回只有 2 级菜单的条目。不返回有 3 级菜单的条目。
            let object = state.menuStruct[state.menu1Index]
            let temp = JSON.parse(JSON.stringify(object))

            let subMenu = temp.child
            let path1 = temp.path
            subMenu = subMenu.filter(item => !item.child || (item.child.length <= 0));
            subMenu.forEach(item => {
                item.path = path1 + item.path
            })

            return subMenu
        },
        getMenu3: (state) => {  // 返回从第二级开始组织的，且含有第3级菜单的结构，是随着路由动态变化的
            let object1 = state.menuStruct[state.menu1Index];
            let temp = JSON.parse(JSON.stringify(object1))

            let subMenu = temp.child    // 二级+三级 菜单
            let path1 = object1.path
            subMenu = subMenu
                .filter(item => {
                    return item.child && (item.child.length > 0)       // 筛掉那些没有第三级菜单的条目。
                });
            subMenu.forEach(item => {
                item.path = path1 + item.path
                item.child.forEach(i => {
                    i.path = item.path + i.path
                })
            })
            return subMenu
        },
        getMenu3Flat: (state) => {
            let object1 = state.menuStruct[state.menu1Index];
            let temp = JSON.parse(JSON.stringify(object1))

            let subMenu = temp.child    // 二级+三级 菜单
            let path1 = object1.path
            subMenu = subMenu
                .filter(item => {
                    return item.child && (item.child.length > 0)       // 筛掉那些没有第三级菜单的条目。
                });

            let list = [];
            subMenu.forEach(item => {
                item.path = path1 + item.path
                item.child.forEach(i => {
                    i.path = item.path + i.path;
                    list.push(i);
                })
            })
            return list;
        },
        mileageChangeTable: (state) => {
            return [...state.mileageChangeInsideTable, ...state.mileageChangeOutsideTable]
        }
    },
    mutations: {
        updateMenu1IndexByPath(state, path) {
            let rootPath = "/" + path.split('/')[1]
            for (let i = 0; i < state.menuStruct.length; i++) {
                if (state.menuStruct[i].path === rootPath) {
                    state.menu1Index = "" + i;
                    break;
                }
            }
        },
        updateMenu1Index(state, e) {
            state.menu1Index = e;
        },
        updateLineId(state, e) {
            state.lineId = e;
        },
        updateTrainId(state, e) {
            state.trainId = e;
        },
        switchLeftNavStatus(state) {
            state.leftNavFold = !state.leftNavFold;
        },
        closeLeftNav(state) {
            state.leftNavFold = true;
        },
        mileageChangeInsideTableAddItem(state, item) {
            state.addItem(state.mileageChangeInsideTable, item);
        },
        mileageChangeOutsideTableAddItem(state, item) {
            state.addItem(state.mileageChangeOutsideTable, item);
        },
        mileageChangeInsideTableRemoveItem(state, item) {
            state.removeItem(state.mileageChangeInsideTable, item)
        },
        mileageChangeOutsideTableRemoveItem(state, item) {
            state.removeItem(state.mileageChangeOutsideTable, item)
        },
        mileageChangeInsideTableClearAll(state) {
            state.mileageChangeInsideTable = [];
        },
        mileageChangeOutsideTableClearAll(state) {
            state.mileageChangeOutsideTable = [];
        },
        mileageChangeOutsideTableClearByTrainId(state, trainId) {
            state.mileageChangeOutsideTable = state.mileageChangeOutsideTable.filter(i => {
                return i.trainId !== trainId;
            })
        }
    },
    actions: {},
    modules: {}
})
