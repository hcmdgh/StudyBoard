<template>
    <el-menu
        default-active="/diary"
        class="el-menu-demo"
        mode="horizontal"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        router>
        <el-menu-item index="/study">学习</el-menu-item>
        <el-menu-item index="/diary">日报</el-menu-item>
        <el-menu-item index="/excerpt">日之录</el-menu-item>
    </el-menu>
    <router-view></router-view>
</template>

<script setup>
</script>

<style>
</style>
