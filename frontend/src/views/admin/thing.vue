<template>
  <div>
    <div class="toolbar">
      <a-input-search v-model:value="keyword" placeholder="按岗位名搜索" style="width: 240px" @search="() => load(1)" />
      <a-button type="primary" @click="openCreate">新增岗位</a-button>
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
          <a-tag :color="record.status === '1' ? 'green' : 'default'">
            {{ record.status === '1' ? '上架' : '下架' }}
          </a-tag>
        </template>
        <template v-else-if="column.key === 'action'">
          <a @click="openEdit(record)">编辑</a>
          <a-divider type="vertical" />
          <a-popconfirm title="确定删除该岗位？" @confirm="remove(record)">
            <a class="danger">删除</a>
          </a-popconfirm>
        </template>
      </template>
    </a-table>

    <a-modal v-model:open="modal.open" :title="modal.id ? '编辑岗位' : '新增岗位'" width="600px" @ok="submit">
      <a-form layout="vertical">
        <a-form-item label="岗位名" required>
          <a-input v-model:value="modal.form.title" />
        </a-form-item>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="薪资">
              <a-input v-model:value="modal.form.salary" placeholder="如 15k-25k" />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="状态">
              <a-select v-model:value="modal.form.status">
                <a-select-option value="1">上架</a-select-option>
                <a-select-option value="2">下架</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="分类">
              <a-select v-model:value="modal.form.classification_id" allow-clear placeholder="选择分类">
                <a-select-option v-for="c in classifications" :key="c.id" :value="c.id">{{ c.title }}</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="公司">
              <a-select v-model:value="modal.form.company_id" allow-clear placeholder="选择公司">
                <a-select-option v-for="c in companies" :key="c.id" :value="c.id">{{ c.name }}</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="岗位描述">
          <a-textarea v-model:value="modal.form.description" :rows="4" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { message } from 'ant-design-vue';
import { listApi, createApi, updateApi, deleteApi } from '/@/api/admin/thing';
import { listApi as classificationListApi } from '/@/api/admin/classification';
import { listApi as companyListApi } from '/@/api/admin/company';

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 70 },
  { title: '岗位名', dataIndex: 'title', key: 'title' },
  { title: '薪资', dataIndex: 'salary', key: 'salary', width: 120 },
  { title: '分类', dataIndex: 'classification_title', key: 'classification_title', width: 120 },
  { title: '公司', dataIndex: 'company_name', key: 'company_name', width: 160 },
  { title: '状态', dataIndex: 'status', key: 'status', width: 90 },
  { title: '操作', key: 'action', width: 140 },
];

const list = ref<any[]>([]);
const loading = ref(false);
const keyword = ref('');
const pagination = reactive({ current: 1, pageSize: 10, total: 0, showSizeChanger: false });
const classifications = ref<any[]>([]);
const companies = ref<any[]>([]);

const load = (page = pagination.current) => {
  loading.value = true;
  pagination.current = page;
  listApi({ page, limit: pagination.pageSize, title: keyword.value })
    .then((res) => {
      list.value = res.data.list;
      pagination.total = res.data.total;
    })
    .catch((err) => message.error(err.msg || '加载失败'))
    .finally(() => (loading.value = false));
};
const onTableChange = (pg: any) => load(pg.current);

const loadOptions = () => {
  classificationListApi({}).then((res) => (classifications.value = res.data)).catch(() => {});
  companyListApi({ page: 1, limit: 1000 }).then((res) => (companies.value = res.data.list)).catch(() => {});
};

const modal = reactive<{ open: boolean; id: number | null; form: any }>({ open: false, id: null, form: {} });

const openCreate = () => {
  modal.id = null;
  modal.form = { title: '', salary: '', status: '1', classification_id: undefined, company_id: undefined, description: '' };
  modal.open = true;
};
const openEdit = (record: any) => {
  modal.id = record.id;
  modal.form = {
    title: record.title,
    salary: record.salary,
    status: record.status,
    classification_id: record.classification_id ?? undefined,
    company_id: record.company_id ?? undefined,
    description: record.description,
  };
  modal.open = true;
};
const submit = () => {
  if (!modal.form.title) {
    message.warn('岗位名不能为空');
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

onMounted(() => {
  load(1);
  loadOptions();
});
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
