<template>
  <div>
    <div class="toolbar">
      <span class="hint">岗位分类维护</span>
      <a-button type="primary" @click="openCreate">新增分类</a-button>
    </div>

    <a-table :columns="columns" :data-source="list" :loading="loading" row-key="id" size="middle">
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

    <a-modal v-model:open="modal.open" :title="modal.id ? '编辑分类' : '新增分类'" @ok="submit">
      <a-form layout="vertical">
        <a-form-item label="分类名" required>
          <a-input v-model:value="modal.form.title" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { listApi, createApi, updateApi, deleteApi } from '/@/api/admin/classification';

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '分类名', dataIndex: 'title', key: 'title' },
  { title: '操作', key: 'action', width: 140 },
];

const list = ref<any[]>([]);
const loading = ref(false);

const load = () => {
  loading.value = true;
  listApi({})
    .then((res) => (list.value = res.data))
    .catch((err) => message.error(err.msg || '加载失败'))
    .finally(() => (loading.value = false));
};

const modal = reactive<{ open: boolean; id: number | null; form: any }>({ open: false, id: null, form: {} });

const openCreate = () => {
  modal.id = null;
  modal.form = { title: '' };
  modal.open = true;
};
const openEdit = (record: any) => {
  modal.id = record.id;
  modal.form = { ...record };
  modal.open = true;
};
const submit = () => {
  if (!modal.form.title) {
    message.warn('分类名不能为空');
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

onMounted(load);
</script>

<style scoped lang="less">
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  .hint {
    color: #6b7280;
  }
}
.danger {
  color: #ef4444;
}
</style>
