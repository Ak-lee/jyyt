<template>
  <div id="header">
    <el-container id="root-container">
      <div id="header-bar">
        <header-main id="logo"/>
        <header-menu class="header-menu"/>
      </div>
      <left-nav id="left-nav"/>
      <div id="container">
        <main-container/>
      </div>
    </el-container>
  </div>
</template>

<script lang="js">
import mainContainer from "@/components/mainContainer";
import headerMain from '@/components/headerMain'
import headerMenu from "@/components/headerMenu";
import leftNav from "@/components/leftNav";

import {mapMutations, mapState} from "vuex";

export default {
  name: 'FirstView',
  data: function () {
    return {}
  },
  components: {
    mainContainer,
    headerMain,
    headerMenu,
    leftNav
  },
  computed: {
    ...mapState['leftNavFold'],
  },
  created() {
    this.updateMenu1IndexByPath(this.$route.path)
  },
  methods: {
    ...mapMutations(['updateMenu1IndexByPath'])
  }
}

</script>

<style>
#header {
}

#left-nav {
  width: 300px;
}

#root-container {
  display: block;
  z-index: 20;
}

#header-bar ::v-deep(.el-tabs__header) {
  margin: 0 !important;
}
</style>