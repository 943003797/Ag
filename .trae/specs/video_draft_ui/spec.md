# 视频草稿生成工具 Spec

## Why
需要一个可视化界面来管理视频草稿的创建、素材上传和AI处理流程。

## What Changes
- 新增Gradio三列布局UI界面 (index.py)
- 新增业务逻辑服务层 (src/service/indexService.py)
- 新增get_cover_prompt函数到LLM模块

## Impact
- Affected specs: 无
- Affected code: index.py, src/service/indexService.py, src/ai_models/big_model/llm.py

## ADDED Requirements
### Requirement: 草稿初始化功能
系统 SHALL 提供通过UI初始化视频草稿目录的功能

#### Scenario: 初始化草稿
- **WHEN** 用户输入主题并点击"初始化草稿"按钮
- **THEN** 系统复制material/baseDraft到drafts/目录下以主题命名的子目录

### Requirement: 视频上传功能
系统 SHALL 提供视频文件上传并保存到草稿目录的功能

#### Scenario: 上传视频
- **WHEN** 用户上传.mp4视频文件
- **THEN** 系统将视频保存到drafts/主题/videoAlg/video.mp4

### Requirement: 配音上传功能
系统 SHALL 提供配音文件上传并保存到草稿目录的功能

#### Scenario: 上传配音
- **WHEN** 用户上传.mp3配音文件
- **THEN** 系统将配音保存到drafts/主题/audioAlg/audio.mp3

### Requirement: ASR语音识别功能
系统 SHALL 提供从视频中提取语音并转换为文字的功能

#### Scenario: ASR解析
- **WHEN** 用户点击"ASR解析"按钮
- **THEN** 系统调用阿里云ASR服务解析视频语音，结果显示在弹幕Prompt文本框中

### Requirement: 封面Prompt生成功能
系统 SHALL 提供根据主题生成图片封面Prompt的功能

#### Scenario: 生成封面Prompt
- **WHEN** ASR解析完成后
- **THEN** 系统调用LLM服务生成封面图片的Prompt，显示在封面Prompt文本框中

### Requirement: 背景音频选择功能
系统 SHALL 提供从预设BGM目录选择背景音频的功能

#### Scenario: 选择背景音频
- **WHEN** 用户从下拉菜单选择背景音频
- **THEN** 系统加载并播放选中的背景音频

## MODIFIED Requirements
### Requirement: LLM模块扩展
扩展现有LLM模块，添加get_cover_prompt方法

## REMOVED Requirements
无
