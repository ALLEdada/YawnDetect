import os
from PIL import Image

# ======== 路径设置（改成你自己的）========
base_dir = r"C:\2025Fall\872AI与交互系统\YawnDetect\Dataset\valid"
ann_file = os.path.join(base_dir, "_annotations.txt")
cls_file = os.path.join(base_dir, "_classes.txt")
train_img_dir = os.path.join(base_dir, "valid")
label_dir = os.path.join(base_dir, "labels", "valid")
os.makedirs(label_dir, exist_ok=True)

# ======== 读取类别文件 ========
with open(cls_file, "r", encoding="utf-8") as f:
    classes = [line.strip() for line in f.readlines() if line.strip()]
print(f"📘 共 {len(classes)} 个类别：{classes}")

# ======== 读取标注文件 ========
with open(ann_file, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

for line in lines:
    try:
        parts = line.split()
        img_name = parts[0]
        coords = parts[1].split(",")
        x1, y1, x2, y2, cls_id = map(float, coords)
        cls_id = int(cls_id)

        img_path = os.path.join(train_img_dir, img_name)
        if not os.path.exists(img_path):
            print(f"⚠️ 找不到图片: {img_path}")
            continue

        # 获取图片尺寸
        with Image.open(img_path) as im:
            w, h = im.size

        # 转换为YOLO格式（中心点与宽高的归一化）
        cx = ((x1 + x2) / 2) / w
        cy = ((y1 + y2) / 2) / h
        bw = (x2 - x1) / w
        bh = (y2 - y1) / h

        # 生成标签文件路径
        label_path = os.path.join(label_dir, os.path.splitext(img_name)[0] + ".txt")
        with open(label_path, "a", encoding="utf-8") as out:
            out.write(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")

    except Exception as e:
        print("❌ 错误行:", line)
        print(e)

print("✅ 所有 YOLO 标签已生成到 labels/train/")

# ======== 生成 YOLO 配置文件 ========
yaml_path = os.path.join(base_dir, "driver_yawn.yaml")
with open(yaml_path, "w", encoding="utf-8") as f:
    f.write(f"path: {base_dir}\n")
    f.write("train: train\n")
    f.write("val: train  # 暂用同一文件夹做验证\n")
    f.write("names:\n")
    for cls in classes:
        f.write(f"  - {cls}\n")
print(f"✅ 已生成配置文件: {yaml_path}")
