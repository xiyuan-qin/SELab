<template>
  <div class="sys-info">
    <a-descriptions title="系统信息" bordered :column="1">
      <a-descriptions-item label="Python 版本">{{ info.python_version || '-' }}</a-descriptions-item>
      <a-descriptions-item label="Django 版本">{{ info.django_version || '-' }}</a-descriptions-item>
      <a-descriptions-item label="操作系统">{{ info.system || '-' }}</a-descriptions-item>
    </a-descriptions>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive } from 'vue';
import { message } from 'ant-design-vue';
import { sysInfoApi } from '/@/api/admin/overview';

const info = reactive<Record<string, string>>({});

onMounted(() => {
  sysInfoApi({})
    .then((res) => Object.assign(info, res.data))
    .catch((err) => message.error(err.msg || '加载失败'));
});
</script>
