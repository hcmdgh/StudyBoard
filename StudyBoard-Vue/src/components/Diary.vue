<template>
    <el-form :model="form">
        <el-form-item label="今日所得">
            <el-input type="textarea" v-model="form.content" rows="5"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submit">保存</el-button>
        </el-form-item>
    </el-form>
    <div>
        <el-card class="box-card" v-for="diary in diaries">
            <template #header>
                <div class="card-header">
                    <span>{{ diary.date }}</span>
                </div>
            </template>
            <div class="text item">
                {{ diary.content }}
            </div>
        </el-card>
    </div>
</template>

<script>
    import { ajaxPost } from './common.vue';
    import { getToken } from './common.vue';

    export default {
        data() {
            return {
                form: {
                    content: '',
                },
                diaries: [],
                token: null,
            };
        },

        methods: {
            refresh() {
                ajaxPost('get-diaries', { token: this.token }, resp => {
                    this.diaries = resp.diaries;
                });
            },

            submit() {
                ajaxPost('update-diary', {
                    token: this.token,
                    content: this.form.content,
                }, resp => {
                    this.refresh();
                });
            },
        },

        mounted() {
            this.token = getToken();
            this.refresh();
        },
    };
</script>

<style scoped>

</style>