import os

image_dir = 'tem_crop_dataset\\unlabel_images_copy'
label_dir = 'tem_crop_dataset\\dataset\\dataset\\labels\\train'

image_exts = ['.jpg', '.png', '.jpeg']

os.makedirs(label_dir, exist_ok=True)

image_files = [f for f in os.listdir(image_dir) if os.path.splitext(f)[1].lower() in image_exts]

count = 0
for img_file in image_files:
    base = os.path.splitext(img_file)[0]
    label_path = os.path.join(label_dir, base + '.txt')
    if not os.path.exists(label_path):
        open(label_path, 'w').close()  
        count += 1

# print(f'give  {count} empty file ') 
print (count)
