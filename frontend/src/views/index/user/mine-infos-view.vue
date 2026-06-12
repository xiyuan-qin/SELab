<template>
  <div class="mine-infos-view nm-card">
    <!-- 头像 + 身份 -->
    <div class="profile">
      <img :src="AvatarImg" class="avatar">
      <div class="meta">
        <h2 class="nick">{{ userStore.user_name || '未登录' }}</h2>
        <span class="nm-role-badge" :class="userStore.isHr ? 'is-hr' : 'is-seeker'">
          {{ userStore.isHr ? '工头 · 招聘方' : '牛马 · 求职者' }}
        </span>
      </div>
    </div>

    <!-- 求职者：两个小统计 -->
    <div v-if="!userStore.isHr" class="stat-row">
      <div class="stat" @click="go('collectThingView')">
        <div class="num">{{ collectCount }}</div>
        <div class="text">收藏的坑</div>
      </div>
      <div class="stat-divider"></div>
      <div class="stat" @click="go('wishThingView')">
        <div class="num">{{ wishCount }}</div>
        <div class="text">心仪的坑</div>
      </div>
    </div>

    <!-- 角色化菜单 -->
    <div v-for="group in menus" :key="group.title" class="menu-group">
      <div class="group-title">{{ group.title }}</div>
      <div
        v-for="item in group.items"
        :key="item.name"
        class="menu-item"
        :class="{ active: route.name === item.name }"
        @click="go(item.name)"
      >
        <span class="dot"></span>
        <div class="labels">
          <span class="main">{{ item.label }}</span>
          <span class="sub">{{ item.sub }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AvatarImg from '/@/assets/images/avatar.jpg'
import { getCollectThingListApi, getWishThingListApi } from '/@/api/index/thing'
import { useUserStore } from '/@/store';

const userStore = useUserStore();
const router = useRouter();
const route = useRoute();

const collectCount = ref(0)
const wishCount = ref(0)

// 招聘方菜单
const HR_MENUS = [
  {
    title: '招聘指挥部',
    items: [
      { name: 'myThingView', label: '坑位管理', sub: '我发布的职位' },
      { name: 'companyPostView', label: '待宰名单', sub: '收到的简历投递' },
      { name: 'myCompanyView', label: '老板档案', sub: '公司信息维护' },
    ],
  },
  {
    title: '账号',
    items: [
      { name: 'userInfoEditView', label: '工头设置', sub: '修改资料' },
      { name: 'securityView', label: '账号安全', sub: '改密码防被卖' },
    ],
  },
]

// 求职者菜单
const SEEKER_MENUS = [
  {
    title: '牛马作战室',
    items: [
      { name: 'resumeEditView', label: '我的卖身契', sub: '编辑简历' },
      { name: 'myPostView', label: '跳坑记录', sub: '我的投递' },
      { name: 'commentView', label: '踩坑日记', sub: '我的评论' },
    ],
  },
  {
    title: '账号',
    items: [
      { name: 'userInfoEditView', label: '牛马设置', sub: '修改资料' },
      { name: 'securityView', label: '账号安全', sub: '改密码防被卖' },
    ],
  },
]

const menus = computed(() => (userStore.isHr ? HR_MENUS : SEEKER_MENUS))

const go = (name: string) => router.push({ name })

onMounted(() => {
  if (userStore.isHr) return
  const username = userStore.user_name
  getCollectThingListApi({ username }).then((res: any) => (collectCount.value = res.data.length)).catch(() => {})
  getWishThingListApi({ username }).then((res: any) => (wishCount.value = res.data.length)).catch(() => {})
})
</script>

<style scoped lang="less">
.mine-infos-view {
  width: 248px;
  flex-shrink: 0;
  padding: 20px 16px;
  height: fit-content;
}

.profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--nm-border);

  .avatar {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid var(--nm-border);
  }
  .nick {
    margin: 0 0 6px;
    font-size: 17px;
    font-weight: 700;
    color: var(--nm-text-main);
    line-height: 1.2;
    word-break: break-all;
  }
}

.stat-row {
  display: flex;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid var(--nm-border);

  .stat {
    flex: 1;
    text-align: center;
    cursor: pointer;
    .num { font-size: 18px; font-weight: 700; color: var(--nm-text-main); }
    .text { font-size: 12px; color: var(--nm-text-sub); margin-top: 2px; }
    &:hover .num { color: var(--nm-primary); }
  }
  .stat-divider { width: 1px; height: 28px; background: var(--nm-border); }
}

.menu-group {
  margin-top: 16px;

  .group-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--nm-text-muted);
    letter-spacing: 0.5px;
    margin-bottom: 6px;
    padding-left: 4px;
  }

  .menu-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: var(--nm-radius);
    cursor: pointer;
    transition: background 0.15s;

    .dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--nm-border-dark);
      flex-shrink: 0;
      transition: background 0.15s;
    }
    .labels { display: flex; flex-direction: column; line-height: 1.3; }
    .main { font-size: 14px; color: var(--nm-text-main); font-weight: 500; }
    .sub { font-size: 11px; color: var(--nm-text-muted); }

    &:hover { background: var(--nm-bg-soft); }
    &.active {
      background: var(--nm-bg-soft);
      .dot { background: var(--nm-primary); }
      .main { color: var(--nm-primary); }
    }
  }
}
</style>
