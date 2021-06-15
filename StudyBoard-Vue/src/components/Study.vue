<template>
    <h1>欢迎来学习，{{ username }}先生~ 今日学习总时长：{{ dailyStudyTime }}</h1>
    <div class="container">
        <label>
            任务描述：
            <input type="text" v-model="input.desc">
        </label>
        <label>
            时长：
            <select v-model="input.duration">
                <option v-for="item in choice.minute" :value="item">{{ item }}</option>
            </select>
            分钟
        </label>
        <button @click="addStudyTask">开始学习</button>
    </div>

    <div class="container" v-if="studyState.studying">
        <div>当前任务：{{ studyState.desc }}</div>
        <div class="time-panel">{{ remainTime }}</div>
        <button @click="giveUp">放弃任务</button>
    </div>
    <div class="container" v-if="!studyState.studying">
        <div>目前没有正在进行的学习任务，赶快学习吧~</div>
    </div>

    <div class="container">
        <table>
            <tr>
                <th>任务描述</th>
                <th>开始时间</th>
                <th>持续时长</th>
            </tr>
            <tr v-for="task in dailyTasks">
                <td>{{ task.desc }}</td>
                <td>{{ task.begin_time }}</td>
                <td>{{ task.duration }} min</td>
            </tr>
        </table>
    </div>
</template>

<script>
    import { ajaxPost } from './common.vue';
    import { getToken } from './common.vue';

    function formatSecond(second) {
        second = Math.max(second, 0);
        const h = Math.floor(second / 3600);
        const m = Math.floor(second / 60) % 60;
        const s = second % 60;

        const hh = h.toString().padStart(2, '0');
        const mm = m.toString().padStart(2, '0');
        const ss = s.toString().padStart(2, '0');

        return hh + ':' + mm + ':' + ss;
    }

    export default {
        data() {
            return {
                input: {
                    desc: '学习',
                    duration: '40',
                },
                choice: {
                    minute: [ 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120 ],
                },
                username: null,
                token: null,
                studyState: {
                    studying: false,
                    desc: '',
                    remainSeconds: 0,
                },
                interval: null,
                dailyStudyTime: '',
                dailyTasks: [],
            }
        },

        methods: {
            addStudyTask() {
                ajaxPost('add-study-task', {
                    token: this.token,
                    duration: parseInt(this.input.duration),
                    desc: this.input.desc,
                }, resp => {
                    if (resp.error === 'studying') {
                        alert("您已经处于一个学习任务中了，一心不能二用哦！");
                    }
                    this.refresh();
                });
            },

            refresh() {
                if (this.interval) {
                    clearInterval(this.interval);
                }

                ajaxPost('get-daily-states', { token: this.token }, dailyStates => {
                    this.dailyStudyTime = dailyStates.duration_str;

                    if (dailyStates.running_task.error === 'not studying') {
                        this.studyState.studying = false;
                    } else {
                        this.studyState.studying = true;
                        this.studyState.desc = dailyStates.running_task.desc;
                        this.studyState.remainSeconds = dailyStates.running_task.remain_seconds;
                        this.interval = setInterval(() => {
                            --this.studyState.remainSeconds;
                            if (this.studyState.remainSeconds <= 0) {
                                const absSecond = Math.abs(this.studyState.remainSeconds);
                                if (absSecond % 5 === 3) {
                                    this.refresh();
                                }
                            }
                        }, 1000);
                    }

                    this.dailyTasks = dailyStates.finished_tasks;
                });
            },

            giveUp() {
                if (confirm('学习贵在坚持，您真的要半途而废吗？')) {
                    ajaxPost('interrupt-task', { token: this.token });
                }
                this.refresh();
            },
        },

        mounted() {
            // 检测登录状态
            this.token = getToken();
            ajaxPost('get-username', { token: this.token }, resp => {
                if (resp.error === 'invalid') {
                    alert("您尚未登录，请先登录！");
                    // TODO
                } else {
                    this.username = resp.username;
                }
            });

            // 加载学习状态
            this.refresh();
        },

        computed: {
            remainTime() {
                return formatSecond(this.studyState.remainSeconds);
            }
        },
    };
</script>

<style scoped>

</style>