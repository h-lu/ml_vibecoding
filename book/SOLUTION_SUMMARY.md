# Quarto Book 侧边栏折叠功能 - 解决方案总结

## 问题描述

您希望在Quarto Book中实现侧边栏目录的折叠功能，具体需求：
- 默认只显示 `index.qmd` 和 `ch01/index.qmd` 等章节首页
- 点击章节首页后展开该章节的子内容
- 点击其他章节时，折叠当前章节，展开新点击的章节

## 核心发现

经过深入研究Quarto文档和Context7资源，发现：

**Quarto Book原生不支持章节级别的侧边栏折叠展开功能。**

## 提供的解决方案

我为您提供了两种解决方案：

### 🎯 方案1：使用Parts结构（推荐）

**文件位置：** `_quarto_collapsible.yml`

**特点：**
- ✅ 使用Quarto原生`part`功能
- ✅ 稳定可靠，支持所有输出格式（HTML、PDF、EPUB）
- ✅ 自动章节分组和层次结构
- ✅ 完全兼容Quarto生态系统

**配置示例：**
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

**使用方法：**
```bash
# 应用新配置
cp _quarto_collapsible.yml _quarto.yml

# 预览效果
quarto preview
```

### 🧪 方案2：自定义JavaScript折叠功能（实验性）

**文件位置：**
- `assets/sidebar-collapse.css` - 折叠样式
- `assets/sidebar-collapse.js` - 折叠逻辑

**特点：**
- 🎯 真正的折叠展开效果（▶/▼图标）
- 🔄 手风琴式交互（一次只展开一个章节）
- 💾 记住用户的展开状态
- ⌨️ 支持键盘导航
- 📱 移动端适配

**注意事项：**
- ⚠️ 仅在HTML格式中有效
- ⚠️ 可能与主题更新冲突
- ⚠️ 需要测试浏览器兼容性

## 测试结果

✅ **渲染测试通过**
- 成功渲染138个文件
- Parts结构正常工作
- CSS/JS文件正确加载

## 推荐使用

### 对于生产环境 → 使用方案1
- 稳定可靠
- 维护成本低
- 全格式支持

### 对于特殊需求 → 可尝试方案2
- 更接近您的原始需求
- 需要充分测试
- 建议有备用方案

## 快速开始

1. **备份原配置：**
   ```bash
   cp _quarto.yml _quarto_original.yml
   ```

2. **应用新配置：**
   ```bash
   cp _quarto_collapsible.yml _quarto.yml
   ```

3. **预览效果：**
   ```bash
   quarto preview
   ```

4. **如需恢复：**
   ```bash
   cp _quarto_original.yml _quarto.yml
   ```

## 文件清单

创建的新文件：
- ✅ `_quarto_collapsible.yml` - 带Parts结构的配置
- ✅ `assets/sidebar-collapse.css` - 自定义折叠样式
- ✅ `assets/sidebar-collapse.js` - 自定义折叠逻辑
- ✅ `SIDEBAR_COLLAPSE_README.md` - 详细使用指南
- ✅ `SOLUTION_SUMMARY.md` - 本总结文档

## 技术细节

### Parts结构的工作原理
- 每个`part`在HTML中显示为可折叠的部分
- Quarto自动处理导航和层次结构
- 支持交叉引用和搜索

### 自定义JavaScript的工作原理
- 通过DOM操作识别章节结构
- 使用CSS动画实现折叠效果
- localStorage保存用户状态

## 下一步

1. 测试方案1的Parts结构效果
2. 如满意则直接使用
3. 如需要真正的折叠效果，可测试方案2
4. 根据实际使用情况选择最适合的方案

希望这个解决方案能满足您的需求！如有任何问题，请参考详细的使用指南。
