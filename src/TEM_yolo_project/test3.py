import os
import random
import shutil

# 修改這裡：放你的資料集路徑
image_dir = 'tem_crop_dataset\dataset\images\\val'   # 你的圖片資料夾
label_dir = 'tem_crop_dataset\dataset\labels\\val'   # 你的標註 txt 資料夾

image_exts = ['.jpg', '.jpeg', '.png']

# 找出所有空圖片（沒有標註檔 or 標註檔為空）
empty_images = []
for file in os.listdir(image_dir):
    name, ext = os.path.splitext(file)
    if ext.lower() in image_exts:
        label_path = os.path.join(label_dir, f"{name}.txt")
        if not os.path.exists(label_path) or os.path.getsize(label_path) == 0:
            empty_images.append(name)

# ✅ 保留 360 張空圖，其餘刪掉
keep_num = 50
if len(empty_images) > keep_num:
    to_remove = random.sample(empty_images, len(empty_images) - keep_num)

    for name in to_remove:
        img_path = None
        for ext in image_exts:
            try_path = os.path.join(image_dir, name + ext)
            if os.path.exists(try_path):
                img_path = try_path
                break
        label_path = os.path.join(label_dir, name + '.txt')

        if img_path and os.path.exists(img_path):
            os.remove(img_path)
        if os.path.exists(label_path):
            os.remove(label_path)

    print(f"✅ 已移除 {len(to_remove)} 張空圖片，現在空圖數約為 {keep_num} 張。")
else:
    print("🎉 空圖片數量已經在目標範圍內，無需刪除。")
