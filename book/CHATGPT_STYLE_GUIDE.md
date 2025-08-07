# ChatGPT 风格的 Quarto Book 配置指南

## 概述

这个配置将您的 Quarto Book 设计成类似 ChatGPT 页面的现代、简洁风格。主要包括：

- 🎨 现代化的视觉设计
- 📚 优化的字体系统
- 💻 改进的代码块显示
- 📱 响应式布局
- 🎯 清晰的阅读体验

## 主要特性

### 字体配置
- **主字体**: Inter（ChatGPT 使用的现代无衬线字体）
- **代码字体**: Monaco, SF Mono, Cascadia Code（等宽字体）
- **字体大小**: 16px 基础大小，1.6 行高
- **字体优化**: 启用字距调整、连字和抗锯齿

### 颜色方案
- **主色调**: 黑色 (#000000)
- **次要颜色**: 灰色 (#6b7280)
- **背景色**: 白色 (#ffffff)
- **表面色**: 浅灰 (#f7f7f8)
- **强调色**: ChatGPT 绿色 (#10a37f)

### 代码块样式
- GitHub 风格的语法高亮
- 深色背景的代码块
- 改进的代码复制功能
- 优化的内联代码样式

## 文件结构

```
book/
├── _quarto.yml           # 主配置文件
├── assets/
│   └── chatgpt-style.scss  # ChatGPT 风格样式
└── CHATGPT_STYLE_GUIDE.md  # 本指南
```

## 使用方法

1. **确保配置正确**：检查 `_quarto.yml` 文件中的主题配置
2. **渲染您的书籍**：运行 `quarto render` 命令
3. **查看效果**：在浏览器中打开生成的 HTML 文件

## 自定义选项

### 修改颜色
在 `book/assets/chatgpt-style.scss` 文件中，您可以修改以下变量：

```scss
// 在 :root 部分修改颜色
:root {
  --chatgpt-primary: #000000;      // 主要文字颜色
  --chatgpt-secondary: #6b7280;    // 次要文字颜色
  --chatgpt-background: #ffffff;   // 背景颜色
  --chatgpt-surface: #f7f7f8;      // 表面颜色
  --chatgpt-border: #e5e5e5;       // 边框颜色
  --chatgpt-accent: #10a37f;       // 强调色
}
```

### 调整字体
在 `_quarto.yml` 文件中修改字体配置：

```yaml
format:
  html:
    mainfont: "您喜欢的字体, fallback字体"
    monofont: "您喜欢的等宽字体, fallback字体"
    fontsize: "16px"  # 调整基础字体大小
    linestretch: 1.6  # 调整行高
```

### 添加暗色模式（可选）
如果您想添加暗色模式支持，可以在 `_quarto.yml` 中配置：

```yaml
format:
  html:
    theme:
      light: [cosmo, assets/chatgpt-style.scss]
      dark: [cosmo, assets/chatgpt-style.scss, assets/chatgpt-dark.scss]
```

然后创建 `assets/chatgpt-dark.scss` 文件定义暗色样式。

## 代码高亮主题

当前使用 GitHub 风格的代码高亮。如果您想尝试其他样式，可以在 `_quarto.yml` 中修改：

```yaml
highlight-style: github  # 可选：pygments, atom-one, breeze, etc.
```

## 响应式设计

这个配置包含了响应式设计，会在不同设备上自动调整：

- **桌面设备**: 最大宽度 1200px，完整功能
- **平板设备**: 自动调整布局和字体大小
- **手机设备**: 优化的移动端体验

## 高级自定义

### 添加自定义组件
您可以在 `chatgpt-style.scss` 文件中添加自己的样式规则：

```scss
/*-- scss:rules --*/

// 您的自定义样式
.my-custom-class {
  // 样式定义
}
```

### 修改代码块样式
如果您想进一步自定义代码块：

```scss
// 修改代码块背景色
pre {
  background-color: #your-color;
  color: #your-text-color;
}

// 修改内联代码样式
code:not(pre code) {
  background-color: #your-inline-bg;
  color: #your-inline-color;
}
```

## 故障排除

### 字体未正确加载
确保在 `_quarto.yml` 的 `include-in-header` 部分包含了字体链接。

### 样式未生效
1. 检查 `assets/chatgpt-style.scss` 文件是否存在
2. 确认 `_quarto.yml` 中的主题配置正确
3. 重新渲染：`quarto render`

### 移动端显示问题
这个配置已经包含了响应式设计，如果仍有问题，可以在样式文件中调整 `@media` 查询。

## 进一步的增强

您还可以考虑添加：

- 🌙 暗色模式支持
- 🔍 改进的搜索功能
- 📊 自定义图表样式
- 🎭 更多的 Callout 块样式
- 🚀 动画效果

## 技术说明

这个配置基于：
- Quarto Book 格式
- Bootstrap 5 Cosmo 主题作为基础
- SCSS/Sass 自定义样式
- 现代 Web 字体技术
- CSS Grid 和 Flexbox 布局

## 反馈与支持

如果您遇到问题或有改进建议，请查阅 Quarto 官方文档或相关社区资源。

---

享受您的新 ChatGPT 风格 Quarto Book！🎉
