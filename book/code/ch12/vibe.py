import torch
import torch.nn as nn
import requests
from PIL import Image
from torchvision import models, transforms
from captum.attr import LayerGradCam, visualization
import matplotlib.pyplot as plt
import numpy as np

# 1. 加载预训练模型
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
model.eval()  # 设置为评估模式

# 2. 图像预处理
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# 3. 加载并预处理图像
image_url = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Zoorashia_elephant.jpg"
image = Image.open(requests.get(image_url, stream=True).raw)
input_tensor = preprocess(image).unsqueeze(0)  # 添加批次维度
input_tensor.requires_grad = True  # 需要梯度计算

# 4. 获取目标层（最后一个卷积层）
target_layer = model.layer4[2].conv3  # ResNet50的最终卷积层

# 5. 初始化Grad-CAM
grad_cam = LayerGradCam(model, target_layer)

# 6. 模型预测获取目标类别
with torch.no_grad():
    output = model(input_tensor)
    predicted_class = output.argmax(dim=1).item()

# 7. 计算归因图
attributions = grad_cam.attribute(
    input_tensor,
    target=predicted_class,
    relu_attributions=True  # 应用ReLU激活
)

# 8. 可视化结果
# 将归因图转换为热力图并上采样到原始图像尺寸
heatmap = attributions.squeeze().cpu().detach().numpy()
heatmap = np.maximum(heatmap, 0)  # 应用ReLU
heatmap /= np.max(heatmap)  # 归一化

# 将热力图从7x7上采样到224x224（原始图像尺寸）
from scipy.ndimage import zoom
heatmap_resized = zoom(heatmap, (224/7, 224/7), order=1)
# 将热力图扩展为三维，与原始图像匹配 (H, W, C)
heatmap_resized = np.expand_dims(heatmap_resized, axis=2)  # 添加通道维度

# 原始图像反标准化
def inverse_normalize(tensor):
    mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
    return tensor * std + mean

original_image = inverse_normalize(input_tensor).squeeze(0).permute(1, 2, 0).cpu().detach().numpy()
original_image = np.clip(original_image, 0, 1)  # 裁剪到[0,1]范围

# 创建子图显示原始图像、热力图和叠加效果
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 显示原始图像
axes[0].imshow(original_image)
axes[0].set_title("Original Image")
axes[0].axis('off')

# 显示热力图
im1 = axes[1].imshow(heatmap_resized.squeeze(), cmap='jet')
axes[1].set_title("Grad-CAM Heatmap")
axes[1].axis('off')
plt.colorbar(im1, ax=axes[1])

# 使用Captum可视化叠加效果
visualization.visualize_image_attr(
    attr=heatmap_resized,
    original_image=original_image,
    method="blended_heat_map",  # 热力图叠加
    sign="positive",
    alpha_overlay=0.7,  # 热力图透明度
    plt_fig_axis=(fig, axes[2]),
    show_colorbar=True,
    title="Grad-CAM Overlay (Predicted: {})".format(
        models.ResNet50_Weights.IMAGENET1K_V1.meta["categories"][predicted_class]
    )
)

plt.tight_layout()
plt.show()