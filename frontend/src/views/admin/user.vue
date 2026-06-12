<template>
  <div>
    <div class="toolbar">
      <a-input-search
        v-model:value="keyword"
        placeholder="按账号搜索"
        style="width: 240px"
        @search="() => load(1)"
      />
      <a-button type="primary" @click="openCreate">新增用户</a-button>
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
        <template v-if="column.key === 'status'">
          <a-tag :color="record.status === '0' ? 'green' : 'red'">
            {{ record.status === '0' ? '正常' : '封禁' }}
          </a-tag>
        </template>
        <template v-else-if="column.key === 'action'">
          <a @click="openEdit(record)">编辑</a>
          <a-divider type="vertical" />
          <a-popconfirm title="确定删除该用户？" @confirm="remove(record)">
            <a class="danger">删除</a>
          </a-popconfirm>
        </template>
      </template>
    </a-table>

    <a-modal v-model:open="modal.open" :title="modal.id ? '编辑用户' : '新增用户'" @ok="submit">
      <a-form layout="vertical">
        <a-form-item label="账号" required>
          <a-input v-model:value="modal.form.username" :disabled="!!modal.id" />
        </a-form-item>
        <a-form-item v-if="!modal.id" label="密码">
          <a-input v-model:value="modal.form.password" placeholder="默认 123456" />
        </a-form-item>
        <a-form-item label="昵称">
          <a-input v-model:value="modal.form.nickname" />
        </a-form-item>
        <a-form-item label="手机">
          <a-input v-model:value="modal.form.mobile" />
        </a-form-item>
        <a-form-item label="邮箱">
          <a-input v-model:value="modal.form.email" />
        </a-form-item>
        <a-form-item label="状态">
          <a-select v-model:value="modal.form.status">
            <a-select-option value="0">正常</a-select-option>
            <a-select-option value="1">封禁</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { listApi, createApi, updateApi, deleteApi } from '/@/api/admin/user';

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 70 },
  { title: '账号', dataIndex: 'username', key: 'username' },
  { title: '昵称', dataIndex: 'nickname', key: 'nickname' },
  { title: '手机', dataIndex: 'mobile', key: 'mobile' },
  { title: '邮箱', dataIndex: 'email', key: 'email' },
  { title: '状态', dataIndex: 'status', key: 'status', width: 90 },
  { title: '注册时间', dataIndex: 'create_time', key: 'create_time' },
  { title: '操作', key: 'action', width: 140 },
];

const list = ref<any[]>([]);
const loading = ref(false);
const keyword = ref('');
const pagination = reactive({ current: 1, pageSize: 10, total: 0, showSizeChanger: false });

const load = (page = pagination.current) => {
  loading.value = true;
  pagination.current = page;
  listApi({ page, limit: pagination.pageSize, username: keyword.value })
    .then((res) => {
      list.value = res.data.list;
      pagination.total = res.data.total;
    })
    .catch((err) => message.error(err.msg || '加载失败'))
    .finally(() => (loading.value = false));
};

const onTableChange = (pg: any) => load(pg.current);

const modal = reactive<{ open: boolean; id: number | null; form: any }>({
  open: false,
  id: null,
  form: {},
});

const openCreate = () => {
  modal.id = null;
  modal.form = { username: '', password: '', nickname: '', mobile: '', email: '', status: '0' };
  modal.open = true;
};

const openEdit = (record: any) => {
  modal.id = record.id;
  modal.form = { ...record };
  modal.open = true;
};

const submit = () => {
  if (!modal.form.username) {
    message.warn('账号不能为空');
    return;
  }
  const req = modal.id
    ? updateApi({ id: modal.id }, modal.form)
    : createApi(modal.form);
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
