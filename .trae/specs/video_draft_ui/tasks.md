# Tasks
- [x] Task 1: 创建业务逻辑服务层 - 实现src/service/indexService.py
  - [x] SubTask 1.1: 实现初始化草稿目录功能 (copy_base_draft)
  - [x] SubTask 1.2: 实现视频文件上传功能 (upload_video)
  - [x] SubTask 1.3: 实现配音文件上传功能 (upload_audio)
  - [x] SubTask 1.4: 实现ASR语音解析功能 (asr_transcribe)
  - [x] SubTask 1.5: 实现获取背景音频列表功能 (get_bgm_list)
- [x] Task 2: 扩展LLM模块 - 在src/ai_models/big_model/llm.py中添加get_cover_prompt方法
- [x] Task 3: 构建Gradio UI界面 - 实现index.py
  - [x] SubTask 3.1: 创建三列布局
  - [x] SubTask 3.2: 实现左侧组件（主题输入、初始化按钮、视频上传/播放、配音上传/播放）
  - [x] SubTask 3.3: 实现中间组件（ASR解析按钮、弹幕Prompt、封面Prompt）
  - [x] SubTask 3.4: 实现右侧组件（背景音频选择、播放、生成草稿按钮）
  - [x] SubTask 3.5: 绑定所有交互事件

# Task Dependencies
- Task 2 必须在 Task 1 完成后进行
- Task 3 必须在 Task 1 和 Task 2 完成后进行
