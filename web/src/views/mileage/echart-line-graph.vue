<template>
  <div style="display: flex; justify-content: center;">
    <el-scrollbar>
      <div ref="myChart" style="width:800px; height:400px;  pointer-events: auto;" id="myChart"></div>
    </el-scrollbar>
  </div>
</template>

<script>

// 折线图组件
import {inject} from "vue";
import {mapGetters} from "vuex";

export default {
  name: "echart-line-graph",
  props: ['data', 'data2', 'trainId'],
  data() {
    this.thisChart = '';
    return {
      options: {
        tooltip: {
          // 当trigger为’item’时只会显示该点的数据，为’axis’时显示该列下所有坐标轴所对应的数据。
          trigger: 'axis',
          show: true,
        },
        title: {
          left: 'center',
          text: '里程增长数据图'
        },
        // toolbox：这是ECharts中的工具栏。内置有导出图片、数据视图、动态类型切换、数据区域缩放、重置五个工具。
        toolbox: {
          // feature 各工具配置项: dataZoom 数据区域缩放;restore 配置项还原; saveAsImage下载为图片;magicType动态类型切换
          feature: {
            dataZoom: {
              yAxisIndex: 'none',  // y轴不缩放，Index默认为0
            },
            saveAsImage: {},
          }
        },
        dataZoom: [
          {
            type: 'inside'
          }
        ],
        xAxis: {
          type: 'time', // category为一级分类,适用于离散的类目数据,
          name: '日期',
          boundaryGap: false,  // 无间隙
          interval: 1,
        },
        yAxis: {
          type: 'value', // 'value' 数值轴，适用于连续数据。
          boundaryGap: [0, '100%'], // 分别表示数据最小值和最大值的延伸范围，可以直接设置数值或者相对的百分比，
        },
        series: [
          {
            name: '里程数据',
            type: 'line',
            smooth: true,  // 开启平滑处理。true的平滑程度相当于0.5
            // symbol: 'none', // 标记的图形。
            sampling: 'average', //  取过滤点的平均值
            itemStyle: {
              normal: {
                color: 'rgb(70,79,255)' //  图形的颜色。
              }
            },
            data: []
          }
        ],
      },
    }
  },
  methods: {
    setOptions(immediate) {
      if (this.mileageChangeTableThisPage.length) {
        let obj2 = {
          name: '修改里程数据',
          type: 'line',
          smooth: true,  // 开启平滑处理。true的平滑程度相当于0.5
          // symbol: 'none', // 标记的图形。
          sampling: 'average', //  取过滤点的平均值
          itemStyle: {
            normal: {
              color: 'blue' //  图形的颜色。
            }
          },
          data: this.data2
        }
        this.options.series = []
        this.options.series.push(obj2);
        let obj1 = {
          name: '里程数据',
          type: 'line',
          smooth: true,  // 开启平滑处理。true的平滑程度相当于0.5
          // symbol: 'none', // 标记的图形。
          sampling: 'average', //  取过滤点的平均值
          itemStyle: {
            normal: {
              color: 'rgba(128, 128, 128, 0.6)' //  图形的颜色。
            }
          },
          lineStyle: {
            type: 'dashed'
          },
          data: this.data
        }
        this.options.series.push(obj1)
      } else {
        this.options.series = []
        let obj1 = {
          name: '里程数据',
          type: 'line',
          smooth: true,  // 开启平滑处理。true的平滑程度相当于0.5
          // symbol: 'none', // 标记的图形。
          sampling: 'average', //  取过滤点的平均值
          itemStyle: {
            normal: {
              color: 'rgb(70,79,255)' //  图形的颜色。
            }
          },
          data: this.data
        }
        this.options.series.push(obj1)
      }
      if (immediate) {
        this.thisChart.setOption(this.options, true); // 立即更新
      } else {
        this.thisChart.setOption(this.options, {  // 懒更新，不会改变当前的 dataZoom
          notMerge: false,
          lazyUpdate: true,
          silent: false,
        });
      }
    }
  },
  watch: {
    data: {
      handler: function (newVal, oldVal) {
        this.setOptions(true);
      },
      deep: true,
    },
    data2: {
      handler: function (newVal, oldVal) {
        if (this.mileageChangeTableThisPage.length) {
          if (newVal.length > this.data.length) {
            this.thisChart.clear();
            this.setOptions(true);
          } else {
            this.setOptions(false);
          }
        } else {
          this.setOptions(true);
        }
      },
      deep: true
    },
  },
  computed: {
    mileageChangeTableThisPage() {
      return this.mileageChangeTable.filter(item => item.trainId === this.trainId)
    },
    ...mapGetters(["mileageChangeTable"])
  },
  mounted() {
    this.echarts = inject("echarts"); // 主要

    const myChart = this.$refs.myChart;  //通过ref获取到DOM节点
    this.thisChart = this.echarts.init(myChart);

    this.setOptions(true);
    this.thisChart.on("click", (params) => {
      let obj = {};
      obj.x = params.data[0];
      obj.y = params.data[1];
      obj.index = params.dataIndex;
      this.$emit("itemClick", obj);
    });
  }

}
</script>

<style scoped>

</style>