<template>
  <div class="portal">
    <Header />
    <div class="hero-banner">
      <div class="hero-inner">
        <img src="/images/banner.png" alt="牛马直聘，更快找到好工作！" class="banner-img" />
        <div class="hero-overlay">
          <div class="hero-slogan">
            <span class="line1">别内卷了</span>
            <span class="line2">找个能喘气的坑先跳进去</span>
          </div>
        </div>
      </div>
    </div>
    <Content />
    <Footer />
  </div>
</template>
<script>
import Header from '/@/views/index/components/header.vue'
import Footer from '/@/views/index/components/footer.vue'
import Content from '/@/views/index/components/content.vue'

export default {
  components: {
    Footer,
    Header,
    Content
  },
  data () {
    return {
    }
  }
}
</script>
<style scoped lang="less">
.hero-banner {
  margin-top: 56px;
  width: 100%;
  background: var(--nm-dark);
  overflow: hidden;
}

.hero-inner {
  max-width: 1100px;
  margin: 0 auto;
  position: relative;
  display: flex;
  align-items: center;
}

.banner-img {
  width: 100%;
  max-height: 220px;
  object-fit: cover;
  object-position: center;
  display: block;
  opacity: 0.92;
}

.hero-overlay {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  padding-right: 48px;
  background: linear-gradient(to left, rgba(28,25,23,0.7) 0%, transparent 100%);
  min-width: 260px;
}

.hero-slogan {
  text-align: right;
  display: flex;
  flex-direction: column;
  gap: 6px;

  .line1 {
    font-size: 28px;
    font-weight: 900;
    color: #fff;
    letter-spacing: 2px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.4);
  }

  .line2 {
    font-size: 14px;
    color: rgba(255,255,255,0.75);
    letter-spacing: 0.5px;
    font-weight: 400;
  }
}
</style>
