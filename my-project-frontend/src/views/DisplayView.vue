<template>
  <div id="container">
    <div id="renderBox" ref="renderBox" style="width: 80%; height: 80vh;"
         @mousedown="startRotate"
         @mouseup="stopRotate"
         @mouseleave="stopRotate"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import * as THREE from 'three';
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const renderBox = ref(null);
let controls, camera, renderer, mesh;

async function downloadFile(url) {
  try {
    const headers = {
      'Authorization': `Bearer ${takeAccessToken()}`,
      'Accept': '*/*'
    };
    const response = await axios.get(url, { headers, responseType: 'blob' });
    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error(`请求失败，状态码: ${response.status}`);
    }
  } catch (error) {
    console.error('下载文件失败:', error);
    ElMessage.error('文件下载失败，请联系管理员');
    throw error;
  }
}

function takeAccessToken() {
  const authItemName = "authorize";
  const str = localStorage.getItem(authItemName) || sessionStorage.getItem(authItemName);
  if (!str) return null;
  const authObj = JSON.parse(str);
  return authObj.token;
}

onMounted(async () => {
  await nextTick();
  initThreeJsScene();
});

onUnmounted(() => {
  controls.dispose();
  window.removeEventListener('mousemove', handleMouseMove);
});

function initThreeJsScene() {
  const scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, renderBox.value.clientWidth / renderBox.value.clientHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(renderBox.value.clientWidth, renderBox.value.clientHeight);
  renderBox.value.appendChild(renderer.domElement);

  // Improved lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 5.0);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(1, 1, 1);
  scene.add(directionalLight);

  camera.position.set(0, 5, 15);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.1;
  controls.enableZoom = true;

  loadPLYFile(scene, camera, renderer);
}

async function loadPLYFile(scene, camera, renderer) {
  try {
    const modelUrl = 'http://localhost:8080/download/scene_dense_mesh_texture.ply';
    const textureUrl = 'http://localhost:8080/download/scene_dense_mesh_texture0.png';

    const [modelBlob, textureBlob] = await Promise.all([
      downloadFile(modelUrl),
      downloadFile(textureUrl)
    ]);

    const loader = new PLYLoader();
    const textureLoader = new THREE.TextureLoader();
    const texture = textureLoader.load(URL.createObjectURL(textureBlob));
    texture.encoding = THREE.sRGBEncoding;  // Ensuring the texture uses sRGB color space

    const geometry = await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsArrayBuffer(modelBlob);
      reader.onloadend = () => {
        resolve(loader.parse(reader.result));
      };
      reader.onerror = reject;
    });

    const material = new THREE.MeshStandardMaterial({
      map: texture,
      metalness: 0.5,
      roughness: 0.3
    });

    mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);
    animate(scene, camera, renderer);
  } catch (error) {
    console.error('加载模型或纹理文件失败:', error.message);
  }
}

function animate(scene, camera, renderer) {
  renderer.render(scene, camera);
  controls.update();
  requestAnimationFrame(() => animate(scene, camera, renderer));
}

function startRotate(event) {
  window.addEventListener('mousemove', handleMouseMove);
}

function stopRotate(event) {
  window.removeEventListener('mousemove', handleMouseMove);
}

function handleMouseMove(event) {
  if (!mesh) return;
  const deltaY = event.movementY;
  const deltaX = event.movementX;

  mesh.rotation.z += deltaX * 0.01;
  mesh.rotation.x += deltaY * 0.01;
}
</script>

<style>
#container {
  width: 100vw;
  height: 100vh;
  background-image: url('https://image.cingta.com//static/image/20200317/d4d6346b60644ece92d8dc3919901b04.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
}
#renderBox {
  width: 60%;
  height: 80%;
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
