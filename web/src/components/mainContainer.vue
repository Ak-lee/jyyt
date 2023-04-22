<template>
  <div id="main-content" :class="{'active': leftNavFold}">
    <div id="tabs-header" :class="{'active': leftNavFold}">
      <el-row style="width: 100%;">
        <div style="width: 100%; display: flex;">
          <el-tabs
              id="tabs"
              @tab-remove="removeTab"
              @tab-change="handleTabChange"
              v-model="editableTabsValue"
              type="card"
              style="width: calc(100% - 40px);"
          >
            <el-tab-pane name="0">
              <template v-slot:label>
                <div id="homeBtnContainer">
                  <div id="homeBtn" @click="handleHomeBtnClick">
                    <svg
                        t="1664439926933"
                        class="icon"
                        viewBox="0 0 1024 1024"
                        version="1.1"
                        xmlns="http://www.w3.org/2000/svg"
                        p-id="5434"
                        width="25"
                        height="25"
                    >
                      <path
                          d="M1014.613212 543.119765c-3.970428 3.806699-9.076726 5.699816-14.172791 5.699816-5.372358 0-10.744715-2.108011-14.766308-6.293333l-64.539922-67.24145 0 523.543917c0 11.307533-9.15859 20.466124-20.466124 20.466124l-265.261433 0c-11.307533 0-20.466124-9.15859-20.466124-20.466124 0-11.2973 9.15859-20.466124 20.466124-20.466124l244.795309 0 0-545.729196-367.233895-382.614188-367.223662 382.593721 0 545.749662 224.329185 0L370.07357 672.353105c0-11.307533 9.168824-20.466124 20.466124-20.466124l244.86694 0c11.2973 0 20.466124 9.15859 20.466124 20.466124 0 11.2973-9.168824 20.466124-20.466124 20.466124l-224.400816 0 0 306.009486c0 11.307533-9.15859 20.466124-20.466124 20.466124l-265.261433 0c-11.2973 0-20.466124-9.15859-20.466124-20.466124L104.812137 475.264331l-64.550155 67.251683c-7.828292 8.15575-20.783349 8.42181-28.939099 0.593518s-8.42181-20.783349-0.593518-28.939099L498.201739 6.293333c3.857864-4.021593 9.18929-6.293333 14.766308-6.293333 5.566786 0 10.898211 2.27174 14.756075 6.293333l487.482607 507.887332C1023.035022 522.336416 1022.768963 535.291472 1014.613212 543.119765z"
                          p-id="5435"
                      ></path>
                    </svg>
                  </div>
                </div>
              </template>
            </el-tab-pane>
            <el-tab-pane
                v-for="(item, index) in items"
                :label="item.label"
                :name="item.name"
                :key="index"
                closable
            >
            </el-tab-pane>
          </el-tabs>
          <el-dropdown style="width: 40px;" trigger="click" id="arrowDownWrapper"
                       placement="bottom-end">
            <div class="arrowDown">
              <el-icon>
                <arrow-down/>
              </el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="removeTab(this.editableTabsValue)"
                >关闭当前标签页
                </el-dropdown-item
                >
                <el-dropdown-item @click="tabsCloseOtherHandle()"
                >关闭其他标签页
                </el-dropdown-item
                >
                <el-dropdown-item @click="tabsCloseAllHandle()"
                >关闭全部标签页
                </el-dropdown-item
                >
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-row>
    </div>
    <div id="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import {mapGetters, mapMutations, mapState} from "vuex";
import {ArrowDown} from "@element-plus/icons-vue";

export default {
  name: "mainContainer",
  data() {
    return {
      items: [],
      editableTabsValue: "0",
      tabIndex: 1,
    };
  },
  components: {
    ArrowDown,
  },
  methods: {
    ...mapMutations(["updateMenu1IndexByPath"]),
    removeTab(targetName) {
      let activeName = this.editableTabsValue; // 目前处于激活状态的 tab index

      if (activeName === targetName) {
        // 要删除的是当前 tab
        this.items.forEach((tab, index) => {
          if (tab.name === targetName) {
            const nextTab = this.items[index + 1] || this.items[index - 1];
            if (nextTab) {
              activeName = nextTab.name;
            }
          }
        });
      }

      this.editableTabsValue = activeName;
      this.items = this.items.filter((tab) => tab.name !== targetName);
      if (this.items.length == 0) {
        this.$router.push("/home");
        this.editableTabsValue = "0";
      }
    },
    handleRouteChange(route) {
      // 分两种情况，一是该tab已经存在，激活即可。
      // 另一种情况，该 tab 不存在，tabIndex++, 并创建 tab
      if (route.path === "/home") {
        return;
      }
      let index = this.items.findIndex((i) => {
        return i.path === route.path;
      });
      if (index !== -1) {
        // 该tab已经存在
        this.editableTabsValue = this.items[index].name;
      } else {
        // 该 tab 不存在，最重要的是拿到该 tab 的 label
        let label;
        if (this.getMenu2.findIndex((i) => i.path == route.path) !== -1) {
          label = this.getMenu2.filter((i) => i.path == route.path)[0].name;
        }
        if (this.getMenu3Flat.findIndex((i) => i.path == route.path) !== -1) {
          label = this.getMenu3Flat.filter((i) => i.path == route.path)[0].name;
        }
        this.items.push({
          label,
          name: ++this.tabIndex,
          path: route.path,
          query: route.query,
          params: route.params,
        });
        this.editableTabsValue = this.tabIndex;
      }
    },
    handleHomeBtnClick() {
      this.$router.push("/home");
      this.editableTabsValue = "0";
    },
    // tabs, 关闭其它
    tabsCloseOtherHandle() {
      this.items = this.items.filter((item) => {
        return item.name === this.editableTabsValue;
      });
    },
    // tabs, 关闭全部
    tabsCloseAllHandle() {
      this.items = [];
      this.editableTabsValue = "0";
      this.$router.push("/home");
    },
    handleTabChange(tabName) {
      var temp = this.items.filter((i) => i.name === tabName);
      if (temp.length > 0) {
        var obj = {}
        var path = temp.at(0);
        if (path.path === this.$route.path) {
          return;
        }
        obj.path = path.path;
        obj.query = path.query;
        obj.param = path.param;
        this.$router.push(obj);
      }
    },
  },
  watch: {
    $route: {
      handler: "handleRouteChange",
      immediate: true,
    },
  },
  computed: {
    ...mapGetters(["getMenu2", "getMenu3", "getMenu3Flat"]),
    ...mapState(["leftNavFold"])
  },
};
</script>

<style scoped>
#main-content {
  /*min-height: 600px;*/
  /*border: 1px solid #9c9c9c;*/
  transition: margin-left 0.3s;
  margin-left: 230px;
  left: 0;
  top: 100px;
  position: relative;
  /*background: rgb(238, 238, 238);*/
  background-color: #e4e7ed;
  transition: margin-left 0.3s;
  padding-bottom: 15px;
}

#main-content.active {
  margin-left: 64px;
}

#tabs {
  width: 100%;
  box-sizing: border-box;
}

#tabs.el-tabs .el-tab-pane {
  width: 100%;
}

#homeBtn {
  cursor: pointer;
  align-self: center;
}

#homeBtn > svg {
  margin-top: 7.5px;
  margin-bottom: -7.5px;
}

#tabs-header {
  display: flex;
  background-color: white;
  text-align: center;
  align-items: center;
  position: fixed;
  top: 60px;
  margin-left: 230px;
  left: 0px;
  right: 0px;
  transition: margin-left 0.3s;
  z-index: 10;
}


#tabs-header.active {
  margin-left: 64px;
}

::v-deep(.is-active) {
  background-color: transparent;
  border-bottom: 2px solid #627ea9 !important;
  color: #627ea9;
}

#tabs-header ::v-deep(.el-tabs__header) {
  margin-bottom: 0px;
}

#tabs-header ::v-deep .el-tabs--card > .el-tabs__header .el-tabs__item {
  border-left: none;
}

#tabs-header::v-deep .el-tabs--card > .el-tabs__header .el-tabs__nav {
  border: none;
}

#tabs-header ::v-deep .el-tabs__item.is-active:first-child {
  border-bottom: none;
}

#tabs-header ::v-deep .el-tabs__item.is-active:first-child svg {
  fill: #627ea9;
}

#tabs-header ::v-deep .el-tabs__item {
  margin: 0 0 !important;
  padding: 0 20px !important;
}

.arrowDown {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-left: 2px solid #e1e1e1;
}

#content {
  margin: 0px 15px;
}
</style>