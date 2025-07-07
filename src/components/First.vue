<template>
  <div class="dashboard-container" style="max-height:44em;overflow:auto;">
    <!-- 顶部统计卡片区域 -->
    <el-row class="stats-cards">
      <!-- 公司总人数卡片 -->
      <div class="sub">
        <el-card @click="jumpAllHuman">
          <template #header>
            <div class="card-header">
              <i class="el-icon-s-custom"></i>
              <span>公司员工总人数</span>
            </div>
          </template>
          <div class="card-content">
            <p class="value" style="font-size:2em;text-align:center">{{ humanTotal }}人</p>

          </div>
        </el-card>
      </div>
      <div class="dept">
        <!-- 部门人数卡片组 -->
        <el-card v-for="(v, i) in deptList" :key="i" class="deptCard" @click="jumpDept(i)">
          <template #header>
            <div>
              <i></i>
              <span>{{ v }}人数 <p class="value">{{ totalList[i] }}人</p></span>

            </div>
          </template>
          <div class="card-content">

          </div>
        </el-card>
      </div>
    </el-row>

    <!-- 个人信息和项目信息区域 -->
    <el-row class="content-row">
      <el-col :span="8">
        <el-card class="performance-card" @click="router.push('/personPerformance')">
          <h4 class="section-title">最新绩效与评分入口</h4>
          <div class="performance-content"> <!-- 新增容器包裹绩效和评分 -->
            <div class="performance-score">
              <div>
                <span>最新绩效:{{ sorce }}</span>
              </div>
              <div class="score-details">
                <p>{{ year }}年度绩效评估</p>
                <p>评级:{{ state }}</p>
              </div>
            </div>

            <div class="rating-entries"> <!-- 评分入口改为上下排布 -->
              <div class="rating-item" @click="router.push('/teamComment')">
                <div class="rating-card">
                  <i class="el-icon-s-claim"></i>
                  <p>项目评分</p>
                </div>
              </div>
              <div class="rating-item" @click="router.push('/deptComment')">
                <div class="rating-card">
                  <i class="el-icon-s-cooperation"></i>
                  <p>部门评分</p>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 右侧部门和绩效卡片 -->
      <el-col :span="8">
        <el-card class="attendance-card" @click="jumpAttend">
          <div class="attendance-info">
            <h4 class="section-title">今日考勤</h4>
            <el-row class="checkin-status" :gutter="20">
              <el-col :span="12">
                <p>上班打卡</p>
                <p class="time-value">{{attd?.checkIn?.map((v, i) => {
                  v = v < 10 ? '0' + v : v; v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v; return v
                }).join('') || "未签到" }}</p>
              </el-col>
              <el-col :span="12">
                <p>下班打卡</p>
                <p class="time-value">{{attd?.checkOut?.map((v, i) => {
                  v = v < 10 ? '0' + v : v; v = i == 2 ? v + ' ' : i < 3 ? v + '-' : i != 5 ? v + ':' : v ;return v
                }).join('') || "未签退" }}</p>
              </el-col>
            </el-row>
            <el-button style="height: 3em;margin-top: 4em;" :disabled="attd?.checkIn&&attd?.checkOut" type="primary" @click="Attend">
              {{ !attd ? '前往签到' : !attd?.checkOut ? '前往签退' : '今日已打卡' }}
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>


  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import api from '../untils/api/count'
import hapi from '../untils/api/human'
import papi from '../untils/api/performance'
import aapi from '../untils/api/attend'
import { useMainDataStore } from '../stores';
import { useRouter } from 'vue-router';
onMounted(async () => {
  humanTotal.value = await api.humanCount().then(({ data }) => data.count)
  totalList.value = []
  totalList.value = await Promise.all(
    deptList.map(async (v, i) => {
      return await hapi.getDeptHuman({ deptId: i + 1 }).then(({ data }) => {
        return data.length
      })
    })
  )
  sorce.value = await papi.getOne({ empId: dstore.uesrInfo.empId, last: '1' }).then(({ data }) => data[0])
  year.value = sorce.value.year
  sorce.value = sorce.value.totalScore
  state.value = callState(sorce.value)
  attd.value = await aapi.getToday(dstore.uesrInfo.empId).then(({ data }) => data)

  
})
const router = useRouter()
const humanTotal = ref('')
const dstore = useMainDataStore()
const deptList = dstore.deptList
const totalList = ref([])
const year = ref('')
const sorce = ref('')
const state = ref('')
const callState = (s) => {
  return s <= 60 ? '差' : s <= 80 ? '中' : s <= 90 ? '良好' : '优秀'
}
const attd = ref([])


const deptProjects = ref([
  { deptName: '运营部', totalProjects: 5, completedProjects: 3, avgScore: 4.2 },

]);
const Attend=async()=>{
   !attd ?await aapi.checkIn(dstore.uesrInfo.empId) : !attd?.checkOut ?await aapi.checkOut(dstore.uesrInfo.empId) : '今日已打卡' 
    attd.value = await aapi.getToday(dstore.uesrInfo.empId).then(({ data }) => data)
}
const jumpAllHuman=()=>{
  dstore.uesrInfo.roleId==1?router.push('/allHuman'):ElMessage({
    type:'warnning',
    message:'无权限'
  })
}
const jumpDept=(i)=>{
  dstore.uesrInfo.roleId!=3&&dstore.uesrInfo.deptId==i+1?router.push('/deptHuman'):ElMessage({
    type:'warnning',
    message:'无权限'
  })
}
const jumpAttend=()=>{
  router.push('/personAttend')
}







</script>

<style lang="less" scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
  max-height: 40em;

  .stats-cards {
    display: flex; // 使用 flex 布局
    flex-wrap: wrap; // 允许换行
    gap: 20px; // 元素之间的间距
    margin-bottom: 20px;

    .sub {
      flex: 0 0 auto; // 不伸缩，不收缩，自动宽度
      width: 25em; // 固定宽度

      .el-card {
        height: 100%; // 卡片高度填满容器
      }
    }

    .dept {
      flex: 1; // 占据剩余空间
      display: flex; // 内部也使用 flex 布局
      flex-wrap: wrap; // 允许换行
      gap: 20px; // 卡片之间的间距

      .deptCard {
        height: 3em;
        width: 100%;

        .el-card__header {
          margin: 0;
          padding: 0; // 减小头部内边距

          .value {
            width: 80%;
            text-align: center;
            display: inline-block;
            font-size: 1em; // 调整字体大小
            font-weight: bold;
            margin: 0;
          }
        }

      }
    }
  }

  .content-row {
    display: flex;
    /* 启用flex布局 */
    gap: 20px;
    /* 卡片间距 */
    margin-bottom: 20px;

    .performance-card,
    .attendance-card {

      flex: 1;
      /* 平均分配空间，高度一致 */
      min-width: 0;

      display: flex;
      /* 内部启用flex布局 */
      flex-direction: column;
      /* 内容垂直排列 */
      height: 100%;
      /* 撑满父容器高度 */
    }

    .performance-card {

      .rating-entries {
        margin-top: auto;
        /* 评分入口固定在卡片底部 */
      }
    }

    .attendance-card {
      width: 52.2em;

      .attendance-info {
        display: flex;
        flex-direction: column;
        height: 100%;
        /* 考勤内容撑满卡片 */

        .checkin-status {
          flex: 1;
          /* 考勤状态占据主要空间 */
        }

        .checkin-btn,
        .checkout-btn {
          margin-top: auto;
          /* 打卡按钮固定在卡片底部 */
        }
      }
    }

    .performance-card {
      .section-title {
        text-align: center;
        /* 标题居中 */
      }

      .performance-content {
        display: flex;
        /* 启用flex布局 */
        flex-wrap: wrap;
        /* 允许换行 */
        gap: 20px;
        /* 绩效与评分间距 */
        padding: 10px 0;
        /* 内部间距 */

        .performance-score {
          flex: 1;
          /* 绩效内容占据主要空间 */
          min-width: 180px;
          /* 最小宽度 */

          .score-circle,
          .score-details {
            /* 原有样式不变 */
          }
        }

        .rating-entries {
          display: flex;
          /* 评分入口容器启用flex */
          flex-direction: column;
          /* 评分入口上下排列 */
          gap: 10px;
          /* 评分项间距 */
          min-width: 120px;
          /* 最小宽度 */

          .rating-item {
            width: 100%;
            /* 评分项占满宽度 */

            .rating-card {
              padding: 15px;
              text-align: center;
              border-radius: 10px;
              background-color: #f5f7fa;
              transition: all 0.3s;

              &:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
              }
            }
          }
        }
      }
    }
  }
}
</style>