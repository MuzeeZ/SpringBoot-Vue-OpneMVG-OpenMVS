<template>
  <!-- 容器，设置全屏背景图，并使内容居中 -->
  <div class="container">
    <!-- 顶部区域，包含退出登录按钮 -->
    <div class="header">
      <el-button @click="userLogout">退出登录</el-button>
    </div>
    <!-- 上传区域，包含上传组件和视频预览 -->
    <div>
      <router-view v-slot="{ Component }">
        <transition name="el-fade-in-linear" mode="out-in">
          <component :is="Component" style="height: 100%"/>
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { post, logout } from '@/net';
import router from "@/router";

const fileInput = ref(null);
const videoSrc = ref('');

function triggerFileInput() {
  if (fileInput.value) {
    console.log('Triggering file input...');
    fileInput.value.click();
  } else {
    console.error("File input ref is not available.");
  }
}

function userLogout() {
  logout(() => {
    router.push("/");
    console.log('User logged out.');
  });
}

function handleSuccess(response, file) {
  console.log('Upload successful:', response);
  ElMessage.success(`文件 ${file.name} 上传成功！`);
  videoSrc.value = URL.createObjectURL(file);
}

function handleError(err) {
  console.error('Upload failed:', err);
  let errorMessage = '文件上传失败。详细信息：未知错误';

  // 检查是否有错误响应并且响应中有数据
  if (err && err.response && err.response.data && err.response.data.message) {
    errorMessage = `文件上传失败。详细信息：${err.response.data.message}`;
  } else if (err && err.message) {
    // 如果响应中没有错误信息，但是错误对象中有消息
    errorMessage = `文件上传失败。详细信息：${err.message}`;
  }

  ElMessage.error(errorMessage);
}


function beforeUpload(file) {
  const isMP4 = file.type === 'video/mp4';
  if (!isMP4) {
    ElMessage.error('只能上传MP4格式的视频文件！');
    return false;
  }
  return true;
}

function uploadFiles(file) {
  console.log('Uploading file:', file);
  if (beforeUpload(file)) {
    const formData = new FormData();
    formData.append('file', file);
    console.log('Form data prepared:', formData.get('file')); // 验证文件是否已添加

    post('http://localhost:8080/upload', formData, data => handleSuccess(data, file), handleError);
  } else {
    console.log('File upload aborted due to format restriction.');
  }
}

function handleVideoChange(file) {
  console.log('File selected:', file);
  if (file) {
    uploadFiles(file);
  } else {
    console.log('No file selected.');
  }
}

onMounted(() => {
  if (!fileInput.value) {
    console.error("fileInput is not mounted.");
  } else {
    console.log("fileInput is successfully mounted.");
  }
});
</script>


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

