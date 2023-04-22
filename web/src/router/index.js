import {createRouter, createWebHashHistory, createWebHistory} from 'vue-router'
import FirstView from '@/views/FirstView'

const routes = [
    {
        path: '/',
        name: 'first',
        component: FirstView,
        redirect: {name: 'home'},
        children: [
            {
                path: 'home',
                name: "home",
                component: () => import("@/components/homeTab")
            },
            {
                path: 'mileage-predict',
                children: [
                    {
                        path: 'history-data-import',
                        name: 'history-data-import',
                        component: () => import('@/components/mileage-predict/history-data-import')
                    },
                    {
                        path: 'predict-res',
                        name: 'predict-res',
                        component: () => import('@/components/mileage-predict/predict-results')
                    }
                ]
            },
            {
                path: 'task',
                children: [
                    {
                        path: 'plan',
                        children: [
                            {
                                path: 'relation',
                                name: 'relation',
                                component: () => import("@/components/task/plan/PlanTypeMapper")
                            },
                            {
                                path: 'year',
                                name: 'year',
                                component: () => import("@/components/task/plan/year")
                            },
                            {
                                path: 'month',
                                name: 'month',
                                component: () => import("@/components/task/plan/month")
                            },
                            {
                                path: 'week',
                                name: 'week',
                                component: () => import("@/components/task/plan/week")
                            },
                            {
                                path: 'day',
                                name: 'day',
                                component: () => import("@/components/task/plan/day")
                            },
                            {
                                path: 'planInquiry',
                                name: 'planInquiry',
                                component: () => import("@/components/task/plan/planInquiry")
                            },
                            {
                                path: 'planFeedback',
                                name: 'planFeedback',
                                component: () => import("@/components/task/plan/planFeedback")
                            },
                            {
                                path: "historyPlanQuery",
                                name: "historyPlanQuery",
                                component: () => import ("@/components/task/plan/historyPlanQuery")
                            },
                        ]
                    },
                    {
                        path: 'transPlan',
                        name: 'transPlan',
                        component: () => import('@/components/task/transPlan')
                    },
                ]
            },
            {
                path: 'line',
                children: [
                    {
                        path: 'yard',
                        children: [
                            {
                                path: 'yard-info',
                                name: 'yard-info',
                                component: () => import('@/components/line/yard/yardInfo')
                            },
                            {
                                path: 'yard-detail',
                                name: 'yard-detail',
                                component: () => import('@/components/line/yard/yardDetail')
                            },
                        ]
                    },
                    {
                        path: 'overhaul',
                        children: [
                            {
                                path: 'type',
                                name: 'type',
                                component: () => import('@/components/line/overhaul/type')
                            },
                            {
                                path: 'typeDetail',
                                name: 'typeDetail',
                                component: () => import('@/components/line/overhaul/taskType-ModeDetail')
                            },
                            {
                                path: 'constraint',
                                name: 'constraint',
                                component: () => import('@/components/line/overhaul/constraint')
                            },
                            {
                                path: 'historyRepairs',
                                name: 'historyRepairs',
                                component: () => import('@/components/line/overhaul/lastRepairs')
                            },
                        ],
                    },
                    {
                        path: 'team',
                        children: [
                            {
                                path: 'skill',
                                name: 'skill',
                                component: () => import('@/components/line/team/skill')
                            },
                        ],
                    },
                    {
                        path: 'basicInfo',
                        name: 'basicInfo',
                        component: () => import('@/components/line/basicInfo')
                    },
                    {
                        path: 'lineDetail',
                        name: 'lineDetail',
                        component: () => import('@/components/line/lineDetail')
                    },
                    {
                        path: 'stationInfo',
                        name: 'stationInfo',
                        component: () => import('@/components/line/stationInfo')
                    },
                    {
                        path: 'trainInfo',
                        name: 'trainInfo',
                        component: () => import('@/components/line/trainInfo')
                    },
                    {
                        path: 'calendar',
                        name: 'calendar',
                        component: () => import("@/components/line/productionCalendar")
                    }
                ]
            },
        ]
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    // history: createWebHashHistory(),
    routes
})

export default router