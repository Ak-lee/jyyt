<template>
  <el-tabs
      id="headerMenutabs"
      v-model="myMenu1Index"
  >

    <div>
      <el-tab-pane
          v-for="(item, index) in menuNames"
          :key="index"
          :label="item"
          :name="''+ index"
      >
      </el-tab-pane>
    </div>
  </el-tabs>
</template>

<script>
import {mapState, mapGetters, mapMutations} from 'vuex'

export default {
  name: "headerMenu",
  computed: {
    ...mapState(['menu1Index']),
    ...mapGetters(['menuNames',]),
    myMenu1Index: {
      get() {
        return this.menu1Index
      },
      set(newVal) {
        this.updateMenu1Index(newVal)
      }
    }
  },
  methods: {
    ...mapMutations(['updateMenu1Index'])
  }
}
</script>


<style scoped>
#headerMenutabs {
  position: fixed !important;
  top: 15px;
  right: 0px;
  /*z-index: 20;*/
  /*float: right;*/
  font-size: 14px;
  color: white;
  font-weight: 600;
  background-color: rgb(37, 60, 82);
  padding-bottom: -10px;
  margin-right: 10px;
  z-index: 20;
}

#headerMenutabs ::v-deep(.el-tabs__header) {
  top: 4px;
  margin-bottom: -15px;
}

#headerMenutabs ::v-deep(.is-active) {
  background-color: #fcfcfc;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  color: black;
}

#headerMenutabs ::v-deep(.el-tabs__item:nth-child(2)) {
  padding-left: 20px;
}

#headerMenutabs ::v-deep(.el-tabs__item:last-child) {
  padding-right: 20px;
}

/deep/ .el-tabs__item {
  color: rgb(228, 231, 237);
  background-color: rgb(37, 60, 82);

}
</style>