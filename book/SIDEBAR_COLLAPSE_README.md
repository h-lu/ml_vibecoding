# Quarto Book 侧边栏折叠功能配置指南

## 概述

由于Quarto Book原生不支持章节级别的侧边栏折叠展开功能，我们提供了两种解决方案来实现您需要的效果。

## 方案1：使用Parts结构（推荐）

这是最接近原生Quarto功能的解决方案，使用`part`配置将每个章节组织为独立的部分。

### 配置方法

使用 `_quarto_collapsible.yml` 配置文件，该文件已经配置好了完整的parts结构：

```yaml
book:
  chapters:
    - index.qmd
    - part: ch01/index.qmd
      chapters:
        - ch01/1_1_crisis_opportunity.qmd
        - ch01/1_2_player_to_designer.qmd
        # ... 其他子章节
    - part: ch02/index.qmd
      chapters:
        - ch02/2_1_business_challenge.qmd
        # ... 其他子章节
```

### 使用方法

1. 备份原始配置：
   ```bash
   cd book
   cp _quarto.yml _quarto_original.yml
   ```

2. 应用新配置：
   ```bash
   cp _quarto_collapsible.yml _quarto.yml
   ```

3. 预览效果：
   ```bash
   quarto preview
   ```

### 优点

- ✅ 使用Quarto原生功能，稳定可靠
- ✅ 在HTML、PDF、EPUB等格式中都能正常工作
- ✅ 自动章节分组和层次结构
- ✅ 支持导航和交叉引用

### 缺点

- ❌ 不是真正的"折叠"效果，而是分组显示
- ❌ 在PDF和EPUB中会显示为"Part"标题

## 方案2：自定义JavaScript折叠功能（实验性）

如果您需要真正的折叠展开效果，我们提供了自定义的CSS和JavaScript解决方案。

### 文件结构

```
book/
├── assets/
│   ├── sidebar-collapse.css    # 折叠样式
│   └── sidebar-collapse.js     # 折叠逻辑
└── _quarto_collapsible.yml     # 配置文件
```

### 功能特性

- ▶️ 章节首页显示折叠/展开图标
- 🔄 点击章节标题切换展开状态
- 📱 自动折叠其他章节（手风琴效果）
- 💾 记住用户的展开状态
- ⌨️ 支持键盘导航
- 📱 移动端适配

### 工作原理

1. **CSS样式** (`sidebar-collapse.css`)：
   - 为章节首页添加折叠图标（▶/▼）
   - 定义子章节的隐藏/显示动画
   - 提供悬停和活跃状态样式

2. **JavaScript逻辑** (`sidebar-collapse.js`)：
   - 自动识别章节首页和子章节
   - 实现折叠/展开交互
   - 处理当前页面高亮
   - 保存用户状态到localStorage

### 使用步骤

1. 确保文件已经创建在正确位置
2. 使用包含CSS和JS的配置文件
3. 渲染并测试效果

### 注意事项

⚠️ **实验性功能**：
- 只在HTML格式中有效
- 可能与主题更新冲突
- 需要测试浏览器兼容性

## 推荐使用方案

### 对于生产环境
建议使用**方案1（Parts结构）**，因为：
- 稳定可靠，不依赖自定义代码
- 支持所有输出格式
- 维护成本低

### 对于演示或特殊需求
如果您特别需要折叠效果，可以尝试**方案2（自定义JavaScript）**，但需要：
- 充分测试各种浏览器
- 准备fallback方案
- 定期检查兼容性

## 切换配置

### 切换到Parts结构：
```bash
cd book
cp _quarto_collapsible.yml _quarto.yml
```

### 恢复原始配置：
```bash
cd book
cp _quarto_original.yml _quarto.yml
```

## 故障排除

### 如果折叠功能不工作

1. 检查文件路径是否正确
2. 验证CSS和JS文件是否加载
3. 查看浏览器控制台错误信息
4. 确认Quarto版本兼容性

### 如果样式冲突

1. 调整CSS选择器优先级
2. 检查主题CSS冲突
3. 使用浏览器开发者工具调试

## 技术支持

如果遇到问题，请检查：
1. Quarto版本是否最新
2. 浏览器是否支持ES6+
3. 网络是否能正常加载资源文件

希望这个解决方案能满足您的需求！
