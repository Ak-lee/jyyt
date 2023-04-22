<template>
  <div class="classi" :class="{'fold' : leftNavFold}">
    <el-scrollbar>
      <!-- 左侧列表 -->
      <el-menu
          id="menuClass"
          ref="menu"
          router
          :collapse="leftNavFold"
      >
        <el-menu-item
            :index="item.path"
            :key="index"
            v-for="(item, index) in getMenu2"
            @click="routeContent(item.path)"
        >
          <el-icon style="font-size: 14px">
            <icon-menu/>
          </el-icon>
          <template #title>{{ item.name }}</template>
        </el-menu-item>
        <el-sub-menu
            :index="'' + index"
            :key="index"
            v-for="(testData, index) in this.getMenu3"
            class="subMenu"
            style="text-align: left"
            id="subMenu"
        >
          <template #title>
            <el-icon>
              <film/>
            </el-icon>
            <span style="font-size: 14px">{{ testData.name }}</span>
          </template>

          <el-menu-item
              :index="item.path"
              :key="index"
              v-for="(item, index) in testData.child"
              @click="routeContent(item.path)"
          >
            <el-icon style="font-size: 14px">
              <icon-menu/>
            </el-icon>
            <span>{{ item.name }}</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script>
import {Film, Menu as iconMenu} from "@element-plus/icons-vue";
import {mapState, mapGetters, mapMutations} from "vuex";

export default {
  data() {
    return {
      fullHeight: 0,
      submenuList: [],
    };
  },
  components: {
    iconMenu,
    Film,
  },
  computed: {
    ...mapGetters(["getMenu2", "getMenu3"]),
    ...mapState(["leftNavFold"]),
  },
  methods: {
    handleSubMenu(arr, parentPath) {
      if (arr.length <= 0) return;
      arr.forEach((item) => {
        item.path = item.path + parentPath;
        this.handleSubMenu(item.child, item.path);
      });
    },
    routeContent() {
    },
    ...mapMutations(['setLeftNavStatus'])
  },
};
</script>

<style lang="css" scoped>

.classi {
  position: fixed;
  width: 230px !important;
  top: 60px !important;
  left: 0;
  bottom: 0;
  float: left;
  overflow: hidden;
  background-color: rgb(37, 60, 82) !important;
  transition: width 0.3s;
  z-index: 10;
}

.classi.fold {
  width: 64px !important;
  transition: width 0.3s;
}

.el-menu ::v-deep(.el-menu-item) {
  background-color: rgb(37, 60, 82);
  height: 40px;
  color: rgb(228, 231, 237);
}

/*子菜单 hover 效果*/
.el-menu /deep/ .el-menu-item:hover {
  color: white;
  /*background-color: rgb(45, 60, 75);*/
  background-color: #387C7A;
}

.el-sub-menu.subMenu > ::v-deep(.el-sub-menu__title) {
  background-color: rgb(37, 60, 82);
  height: 40px;
  color: rgb(228, 231, 237);
}

.el-sub-menu.subMenu > ::v-deep(.el-sub-menu__title):hover {
  background-color: #387C7A;
}

::v-deep(.el-menu) {
  border: none;
}
</style>

<style lang="css">
.el-menu--vertical.el-menu--popup-container .el-menu-item{
  height: 40px;
}
</style>
