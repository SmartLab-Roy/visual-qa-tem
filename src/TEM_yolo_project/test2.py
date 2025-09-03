import os

# 修改這裡：放你的資料集路徑
image_dir = 'tem_crop_dataset/dataset/images/val'   # 你的圖片資料夾
label_dir = 'tem_crop_dataset/dataset/labels/val'   # 你的標註 txt 資料夾

# 允許的圖片副檔名
image_exts = ['.jpg', '.jpeg', '.png']

total_images = 0
empty_labels = 0

for file in os.listdir(image_dir):
    name, ext = os.path.splitext(file)
    if ext.lower() in image_exts:
        total_images += 1
        label_path = os.path.join(label_dir, f"{name}.txt")
        
        # 沒有標註檔 或 是空檔
        if not os.path.exists(label_path) or os.path.getsize(label_path) == 0:
            empty_labels += 1

# 結果輸出
print(f"📦 總圖片數量：{total_images}")
print(f"❌ 空標註圖片數量：{empty_labels}")
if total_images > 0:
    print(f"📊 空圖片比例：{empty_labels / total_images * 100:.2f}%")
else:
    print("⚠️ 找不到任何圖片！請檢查 image_dir 是否正確")
