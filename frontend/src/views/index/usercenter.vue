<template>
  <div class="nm-page user-center">
    <Header />

    <div class="nm-container user-content">
      <aside class="left">
        <MineInfosView />
      </aside>
      <main class="right nm-card">
        <router-view />
      </main>
    </div>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from '/@/views/index/components/header.vue'
import Footer from '/@/views/index/components/footer.vue'
import MineInfosView from '/@/views/index/user/mine-infos-view.vue'
</script>

<style scoped lang="less">
.user-center {
  display: flex;
  flex-direction: column;
}

.user-content {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 20px;
  padding-top: 28px;
  padding-bottom: 48px;

  .left {
    flex-shrink: 0;
  }
  .right {
    flex: 1;
    min-width: 0;
    padding: 24px 28px;
    min-height: 520px;
  }
}
</style>
