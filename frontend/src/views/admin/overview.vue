<template>
  <div class="overview">
    <a-row :gutter="16">
      <a-col v-for="item in cards" :key="item.key" :span="6" class="card-col">
        <a-card :bordered="false" class="stat-card">
          <div class="stat-label">{{ item.label }}</div>
          <div class="stat-value">{{ counts[item.key] ?? 0 }}</div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from 'vue';
import { message } from 'ant-design-vue';
import { listApi } from '/@/api/admin/overview';

const cards = [
  { key: 'user_count', label: '用户数' },
  { key: 'thing_count', label: '岗位数' },
  { key: 'company_count', label: '公司数' },
  { key: 'resume_count', label: '简历数' },
  { key: 'order_count', label: '投递数' },
  { key: 'comment_count', label: '评论数' },
  { key: 'notice_count', label: '公告数' },
  { key: 'classification_count', label: '分类数' },
];

const counts = reactive<Record<string, number>>({});

onMounted(() => {
  listApi({})
    .then((res) => Object.assign(counts, res.data))
    .catch((err) => message.error(err.msg || '加载失败'));
});
</script>

<style scoped lang="less">
.card-col {
  margin-bottom: 16px;
}
.stat-card {
  background: #f9fafb;
  border-radius: 8px;
  .stat-label {
    color: #6b7280;
    font-size: 14px;
  }
  .stat-value {
    margin-top: 8px;
    font-size: 30px;
    font-weight: 700;
    color: #ea580c;
  }
}
</style>
