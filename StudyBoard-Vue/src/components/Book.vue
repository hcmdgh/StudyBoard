<template>
    <el-table
        :data="bookRecords"
        stripe
        style="width: 100%">
        <el-table-column
            prop="name"
            label="书名"
            width="300">
        </el-table-column>
        <el-table-column
            prop="author"
            label="作者"
            width="300">
        </el-table-column>
        <el-table-column
            prop="date"
            label="完成时间"
            width="180">
        </el-table-column>
    </el-table>
</template>

<script>
    import { ajaxPost } from './common.vue';
    import { getToken } from './common.vue';

    export default {
        data() {
            return {
                bookRecords: [],
            };
        },

        methods: {
            refresh() {
                ajaxPost('get-book-records', { token: this.token }, resp => {
                    this.bookRecords = resp.book_records;
                });
            },
        },

        mounted() {
            this.token = getToken();
            this.refresh();
        },
    }
</script>

<style scoped>

</style>