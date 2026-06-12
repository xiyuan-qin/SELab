<template>
  <div>
    <div class="toolbar">
      <a-input-search v-model:value="keyword" placeholder="按公司名搜索" style="width: 240px" @search="() => load(1)" />
      <a-button type="primary" @click="openCreate">新增公司</a-button>
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
          <a @click="openEdit(record)">编辑</a>
          <a-divider type="vertical" />
          <a-popconfirm title="确定删除？" @confirm="remove(record)">
            <a class="danger">删除</a>
          </a-popconfirm>
        </template>
      </template>
    </a-table>

    <a-modal v-model:open="modal.open" :title="modal.id ? '编辑公司' : '新增公司'" @ok="submit">
      <a-form layout="vertical">
        <a-form-item label="公司名" required>
          <a-input v-model:value="modal.form.name" />
        </a-form-item>
        <a-form-item label="规模">
          <a-input v-model:value="modal.form.scale" placeholder="如 100-499 人" />
        </a-form-item>
        <a-form-item label="地址">
          <a-input v-model:value="modal.form.address" />
        </a-form-item>
        <a-form-item label="简介">
          <a-textarea v-model:value="modal.form.description" :rows="4" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { listApi, createApi, updateApi, deleteApi } from '/@/api/admin/company';

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 70 },
  { title: '公司名', dataIndex: 'name', key: 'name' },
  { title: '规模', dataIndex: 'scale', key: 'scale', width: 130 },
  { title: '地址', dataIndex: 'address', key: 'address' },
  { title: '创建时间', dataIndex: 'create_time', key: 'create_time', width: 180 },
  { title: '操作', key: 'action', width: 140 },
];

const list = ref<any[]>([]);
const loading = ref(false);
const keyword = ref('');
const pagination = reactive({ current: 1, pageSize: 10, total: 0, showSizeChanger: false });

const load = (page = pagination.current) => {
  loading.value = true;
  pagination.current = page;
  listApi({ page, limit: pagination.pageSize, name: keyword.value })
    .then((res) => {
      list.value = res.data.list;
      pagination.total = res.data.total;
    })
    .catch((err) => message.error(err.msg || '加载失败'))
    .finally(() => (loading.value = false));
};
const onTableChange = (pg: any) => load(pg.current);

const modal = reactive<{ open: boolean; id: number | null; form: any }>({ open: false, id: null, form: {} });

const openCreate = () => {
  modal.id = null;
  modal.form = { name: '', scale: '', address: '', description: '' };
  modal.open = true;
};
const openEdit = (record: any) => {
  modal.id = record.id;
  modal.form = { ...record };
  modal.open = true;
};
const submit = () => {
  if (!modal.form.name) {
    message.warn('公司名不能为空');
    return;
  }
  const req = modal.id ? updateApi({ id: modal.id }, modal.form) : createApi(modal.form);
  req
    .then(() => {
      message.success(modal.id ? '已更新' : '已创建');
      modal.open = false;
      load();
    })
    .catch((err) => message.error(err.msg || '操作失败'));
};
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
  justify-content: space-between;
  margin-bottom: 16px;
}
.danger {
  color: #ef4444;
}
</style>
