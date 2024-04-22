<template>
  <div class="upload-area" v-loading="uploading">
    <input
        type="file"
        accept="video/*"
        @change="handleVideoChange($event.target.files[0])"
        style="display: none;"
        ref="fileInput" />
    <el-button
        size="large"
        type="primary"
        style="min-width: 200px; margin-bottom: 10px;"
        @click="triggerFileInput">
      点击上传视频
    </el-button>
    <div class="el-upload__tip">只支持MP4格式的视频文件</div>
    <div v-if="videoSrc" class="video-preview">
      <video controls :src="videoSrc">
        Your browser does not support the video tag.
      </video>
    </div>
    <div v-else class="video-placeholder">
      视频预览将显示在这里
    </div>
    <el-button
        size="large"
        type="success"
        style="min-width: 200px; margin-top: 20px;"
        @click="initiate3DReconstruction">
      开始三维重建
    </el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { post } from '@/net';  // 假设这是您之前定义的axios封装

const fileInput = ref(null);
const videoSrc = ref('');
const uploading = ref(false);
const router = useRouter();

function triggerFileInput() {
  fileInput.value.click();
}

function handleVideoChange(file) {
  if (file) {
    uploading.value = true;
    const reader = new FileReader();
    reader.onload = (e) => {
      videoSrc.value = e.target.result;
      uploading.value = false;
    };
    reader.readAsDataURL(file);
  }
}

function initiate3DReconstruction() {
  uploading.value = true;
  router.push('/index/loading').then(() => {
    post('http://localhost:8080/api/reconstruction/start', {},
        (response) => {  // 成功回调
          uploading.value = false;
          // 假设任何从 post 返回的调用都是成功的
          router.push('/display');  // 正确的路由
        },
        (error) => {  // 错误回调
          uploading.value = false;
          // 更详细的错误处理
          if (error.response && error.response.data && error.response.data.message) {
            ElMessage.error('请求重建失败: ' + error.response.data.message);
          } else if (error.message) {
            ElMessage.error('请求重建失败: ' + error.message);
          } else {
            ElMessage.error('请求重建失败: 未知错误');
          }
        }
    );
  });
}
</script>

<style scoped>
.upload-area {
  /* CSS 样式 */
}
.video-preview video {
  width: 100%;
}
.video-placeholder {
  width: 100%;
  height: 300px; /* 调整为合适的尺寸 */
  background-color: #eee;
  text-align: center;
  line-height: 300px;
}
</style>


<style scoped>
.video-preview video {
  max-width: 100%; /* 使视频的宽度不超过其容器的宽度 */
  max-height: 100%;
  //height: auto;   /* 高度自动调整以保持视频的宽高比 */
}
.container {
  width: 100vw;
  height: 100vh;
  background: url('https://image.cingta.com//static/image/20200317/d4d6346b60644ece92d8dc3919901b04.jpg') center center no-repeat;
  background-size: cover;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0.8;
}
.header {
  position: absolute;
  top: 10px;
  right: 30px;
}
.upload-area {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  text-align: center;
  width: auto;
}
.el-upload__tip {
  margin-top: 10px;
  color: #999;
}
.video-preview {
  width: 480px;
  height: 270px;
  overflow: hidden;
  margin-top: 20px;
}
.video-placeholder {
  width: 480px;
  height: 270px;
  line-height: 270px;
  text-align: center;
  background-color: #f0f0f0;
  color: #ccc;
  margin-top: 20px;
  border: 1px dashed #ccc;
}
</style>