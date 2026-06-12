<template>
  <div>
    <div class="toolbar">
      <a-input-search v-model:value="keyword" placeholder="按内容搜索" style="width: 240px" @search="() => load(1)" />
    </div>

    <a-table
      :columns="columns"
      :data-source="list"
      :loading="loading"
      :pagination="pagination"
      row-key="id"
      size="middle"
      @change="onTableChange"
    >
      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'action'">
          <a-popconfirm title="确定删除该评论？" @confirm="remove(record)">
            <a class="danger">删除</a>
          </a-popconfirm>
        </template>
      </template>
    </a-table>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { listApi, deleteApi } from '/@/api/admin/comment';

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 70 },
  { title: '评论内容', dataIndex: 'content', key: 'content', ellipsis: true },
  { title: '评论人', dataIndex: 'user_name', key: 'user_name', width: 140 },
  { title: '所属岗位', dataIndex: 'thing_title', key: 'thing_title' },
  { title: '点赞', dataIndex: 'like_count', key: 'like_count', width: 80 },
  { title: '时间', dataIndex: 'create_time', key: 'create_time', width: 180 },
  { title: '操作', key: 'action', width: 100 },
];

const list = ref<any[]>([]);
const loading = ref(false);
const keyword = ref('');
const pagination = reactive({ current: 1, pageSize: 10, total: 0, showSizeChanger: false });

const load = (page = pagination.current) => {
  loading.value = true;
  pagination.current = page;
  listApi({ page, limit: pagination.pageSize, keyword: keyword.value })
    .then((res) => {
      list.value = res.data.list;
      pagination.total = res.data.total;
    })
    .catch((err) => message.error(err.msg || '加载失败'))
    .finally(() => (loading.value = false));
};
const onTableChange = (pg: any) => load(pg.current);

const remove = (record: any) => {
  deleteApi({ id: record.id })
    .then(() => {
      message.success('已删除');
      load();
    })
    .catch((err) => message.error(err.msg || '删除失败'));
};

onMounted(() => load(1));
</script>

<style scoped lang="less">
.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}
.danger {
  color: #ef4444;
}
</style>
