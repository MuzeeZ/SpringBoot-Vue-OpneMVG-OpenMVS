import cv2
import os
import subprocess

def extract_frames(video_path, output_folder, frames_per_second):
    """ 从视频中按照指定频率提取帧 """
    if not os.path.exists(video_path):
        print("错误：视频文件不存在。")
        return 0

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("错误：无法打开视频文件。")
        return 0

    fps = cap.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
    frame_interval = int(fps / frames_per_second) if frames_per_second > 0 else int(fps)

    frame_count = 0
    frame_number = 0  # 当前帧的编号
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 按照指定的频率保存帧
        if frame_number % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_count += 1
        
        frame_number += 1

    cap.release()
    print(f"总共提取了 {frame_count} 帧。")
    return frame_count

def run_openMVG(image_folder, output_folder, video_name):
    """ 使用openMVG进行SfM """
    matches_dir = os.path.join(output_folder, "matches")
    reconstruction_dir = os.path.join(output_folder, "reconstruction_sequential")
    os.makedirs(matches_dir, exist_ok=True)
    os.makedirs(reconstruction_dir, exist_ok=True)
    
    # 指定 camera_sensor_database.txt 的完整路径
    camera_sensor_db_path = "openMVG/src/openMVG/exif/sensor_width_database/sensor_width_camera_database.txt"

    # 初始化相机文件和稀疏重建
    subprocess.run(["openMVG_main_SfMInit_ImageListing", "-i", image_folder, "-o", matches_dir, "-d", camera_sensor_db_path], check=True)
    
    # 特征提取阶段，调整 describerPreset 为 ULTRA，以尝试获取更多的特征点
    subprocess.run(["openMVG_main_ComputeFeatures", "-i", matches_dir + "/sfm_data.json", "-o", matches_dir, "--describerMethod", "AKAZE_FLOAT", "--describerPreset", "ULTRA"], check=True)
    
    # 匹配特征点
    subprocess.run(["openMVG_main_ComputeMatches", "-i", matches_dir + "/sfm_data.json", "-o", matches_dir], check=True)

    return reconstruction_dir

def run_openMVS(reconstruction_dir, output_folder, video_name):
    """ 使用openMVS进行密集重建和纹理化 """
    mvs_file = os.path.join(reconstruction_dir, "sfm_data.bin")
    subprocess.run(["openMVG_main_openMVG2openMVS", "-i", reconstruction_dir + "/sfm_data.bin", "-o", mvs_file], check=True)

    scene_file = os.path.join(output_folder, video_name + ".mvs")
    subprocess.run(["DensifyPointCloud", mvs_file, "-o", scene_file], check=True)
    mesh_file = os.path.join(output_folder, video_name + ".ply")
    texture_file = os.path.join(output_folder, video_name + "_texture.jpg")
    subprocess.run(["ReconstructMesh", scene_file, "-o", mesh_file], check=True)
    subprocess.run(["TextureMesh", mesh_file, "-o", texture_file], check=True)

def process_video(video_path, output_folder, video_name, frames_per_second):
    """ 处理视频文件，并根据给定的抽帧频率提取帧 """
    frame_folder = os.path.join(output_folder, "frames")
    os.makedirs(frame_folder, exist_ok=True)

    print("正在从视频提取帧...")
    frame_count = extract_frames(video_path, frame_folder, frames_per_second)
    if frame_count == 0:
        return  # 如果帧提取失败，提前终止


if __name__ == "__main__":
    video_path = "video/video.mp4"
    output_folder = "output"
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    process_video(video_path, output_folder, video_name, 2)

