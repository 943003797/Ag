# 封面模板选择器重构计划

## 目标
将竖版模板和横版模板的两个下拉框合并为一个"选择模板"下拉框，根据选择的文件夹自动加载对应的竖版/横版模板图片。

## 修改步骤

### 1. 修改 `get_templates_list()` 函数
- 扫描 `material/baseCover` 目录
- 获取该目录下的所有文件夹名
- 返回文件夹名列表

### 2. 添加新函数 `get_template_images(folder_name)`
- 参数：文件夹名
- 返回：包含竖版和横版模板路径的元组 `(vertical_path, horizontal_path)`
- 逻辑：
  - 竖版模板路径：`material/baseCover/{folder_name}/竖版.png`
  - 横版模板路径：`material/baseCover/{folder_name}/横板.png`
  - 如果文件不存在返回 None

### 3. 修改 UI 布局
- 移除现有的两个模板下拉框（竖版模板、横版模板）
- 添加一个新的"选择模板"下拉框，列出文件夹名
- 保留两个模板预览区（竖版预览、横版预览）

### 4. 添加模板切换事件处理
- 当选择模板文件夹时：
  - 调用 `get_template_images()` 获取竖版和横版模板路径
  - 更新竖版预览图
  - 更新横版预览图

### 5. 修改生成函数调用
- `generate_cover_vertical` 和 `generate_cover_horizontal` 需要根据选择的文件夹名动态构建模板路径
- 修改模板路径构建逻辑：
  - 竖版：`material/baseCover/{folder_name}/竖版.png`
  - 横版：`material/baseCover/{folder_name}/横板.png`

## 文件修改清单
- `d:\AI\Ag\cover_ui.py`
