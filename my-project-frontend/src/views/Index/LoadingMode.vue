<template>
  <div class="loading-area">
    <div class="video-preview">
      <img src="https://gd-hbimg.huaban.com/56304c99a2bcddbac5c5e9b38b5a6ac900ebd896a6015-dywV53_fw1200" alt="Loading" class="loading-gif">
    </div>
    <div class="video-preview">
      <img src="https://s1.aigei.com/src/img/gif/a9/a91013eacc5f46f796772de166b79b82.gif?imageMogr2/auto-orient/thumbnail/!282x282r/gravity/Center/crop/282x282/quality/85/%7CimageView2/2/w/282&e=1735488000&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:xrKari6fssrdvDiS6K8xnr67_fk=" alt="Loading" class="loading-gif">
    </div>
  </div>
</template>

<script setup>
// 不需要在此脚本中特别处理，因为 loading 是纯样式
</script>

<style scoped>
.loading-area {
  width: 480px; /* 与上传控件相同 */
  height: 270px; /* 与上传控件相同 */
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.loading-content {
  width: 100%;
  height: 100%;
  position: relative;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center; /* 在垂直方向上居中对齐子元素 */
  align-items: center; /* 在水平方向上居中对齐子元素 */
}
.loading-text {
  /* 删除原有的定位样式 */
  color: #555;
  font-size: 14px;
}
.loading-gif {
  max-width: 100%;
  max-height: 100%;
}
.video-preview {
  width: 480px;
  height: 270px;
  overflow: hidden;
  margin-top: 20px;
}
</style>






