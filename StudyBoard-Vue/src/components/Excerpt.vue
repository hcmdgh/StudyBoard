<template>
    <el-form :model="form">
        <el-form-item>
            <el-input type="textarea" v-model="form.content" rows="5"></el-input>
        </el-form-item>
        <el-form-item label="来源：">
            <el-input v-model="form.source"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submit">保存</el-button>
        </el-form-item>
    </el-form>
    <div>
        <el-card class="box-card" v-for="excerpt in excerpts">
            <template #header>
                <div class="card-header">
                    <span>{{ excerpt.date }}</span>
                </div>
            </template>
            <div class="text item">
                {{ excerpt.content }}
            </div>
            <div class="text item" style="text-align: right">
                ——{{ excerpt.source }}
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
                    source: '',
                },
                excerpts: [],
                token: null,
            };
        },

        methods: {
            refresh() {
                ajaxPost('get-excerpts', { token: this.token }, resp => {
                    this.excerpts = resp.excerpts;
                });
            },

            submit() {
                ajaxPost('update-excerpt', {
                    token: this.token,
                    content: this.form.content,
                    source: this.form.source,
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