<template>
  <div>
    <div class="toolbar">
      <a-input-search v-model:value="keyword" placeholder="按姓名搜索" style="width: 240px" @search="() => load(1)" />
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
          <a-popconfirm title="确定删除该简历？" @confirm="remove(record)">
            <a class="danger">删除</a>
          </a-popconfirm>
        </template>
      </template>
    </a-table>

    <a-modal v-model:open="modal.open" title="编辑简历" width="600px" @ok="submit">
      <a-form layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="姓名" required>
              <a-input v-model:value="modal.form.name" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="手机">
              <a-input v-model:value="modal.form.mobile" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="学历">
              <a-input v-model:value="modal.form.education" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="工作年限">
              <a-input v-model:value="modal.form.experience" />
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="邮箱">
          <a-input v-model:value="modal.form.email" />
        </a-form-item>
        <a-form-item label="简历内容">
          <a-textarea v-model:value="modal.form.content" :rows="4" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { listApi, updateApi, deleteApi } from '/@/api/admin/resume';

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 70 },
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '所属用户', dataIndex: 'user_name', key: 'user_name' },
  { title: '学历', dataIndex: 'education', key: 'education', width: 110 },
  { title: '工作年限', dataIndex: 'experience', key: 'experience', width: 110 },
  { title: '手机', dataIndex: 'mobile', key: 'mobile' },
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

const openEdit = (record: any) => {
  modal.id = record.id;
  modal.form = { ...record };
  modal.open = true;
};
const submit = () => {
  if (!modal.form.name) {
    message.warn('姓名不能为空');
    return;
  }
  updateApi({ id: modal.id }, modal.form)
    .then(() => {
      message.success('已更新');
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
  justify-content: flex-end;
  margin-bottom: 16px;
}
.danger {
  color: #ef4444;
}
</style>
