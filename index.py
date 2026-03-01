import gradio as gr
import os
from src.service.indexService import (
    copy_base_draft,
    upload_video,
    asr_transcribe,
    get_cover_prompt_from_llm,
    get_bgm_list,
    get_bgm_path,
    extract_audio_from_video,
    get_audio_path,
    DRAFT_DIR
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATERIAL_DIR = os.path.join(BASE_DIR, "material")


def get_video_path(topic):
    if not topic or not topic.strip():
        return None
    video_path = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "videoAlg", "video.mp4")
    if os.path.exists(video_path):
        return video_path
    return None


def get_audio_path(topic):
    if not topic or not topic.strip():
        return None
    audio_path = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "audioAlg", "audio.mp3")
    if os.path.exists(audio_path):
        return audio_path
    return None


def handle_init_draft(topic):
    result = copy_base_draft(topic)
    
    if not topic or not topic.strip():
        return result, None, None, None
    
    from src.service.indexService import DRAFT_DIR
    
    video_path = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "videoAlg", "video.mp4")
    audio_path = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "audioAlg", "audio.mp3")
    asr_path = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "data", "asr.json")
    
    video_player_path = video_path if os.path.exists(video_path) else None
    audio_player_path = audio_path if os.path.exists(audio_path) else None
    asr_file_path = asr_path if os.path.exists(asr_path) else None
    
    return result, video_player_path, audio_player_path, asr_file_path


def handle_upload_video(topic, video_file):
    return upload_video(topic, video_file)


def handle_asr_parse(topic, danmu_prompt):
    if not topic or not topic.strip():
        return danmu_prompt, "错误：主题不能为空"
    
    from src.service.indexService import DRAFT_DIR
    audio_path = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "audioAlg", "audio.mp3")
    print(f"[DEBUG] ASR解析 - 主题: {topic}, DRAFT_DIR: {DRAFT_DIR}, 音频路径: {audio_path}, 存在: {os.path.exists(audio_path)}")
    
    result = asr_transcribe(topic)
    
    if result and not result.startswith("错误") and not result.startswith("ASR"):
        cover_prompt = get_cover_prompt_from_llm(topic)
        return result, cover_prompt
    
    return danmu_prompt, result


def handle_download_asr(topic):
    if not topic or not topic.strip():
        return None
    
    from src.service.indexService import DRAFT_DIR
    asr_json_path = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "data", "asr.json")
    
    if not os.path.exists(asr_json_path):
        return "错误：ASR文件不存在，请先进行ASR解析"
    
    return asr_json_path


def handle_update_keyword(topic, keyword_content):
    if not topic or not topic.strip():
        return "错误：主题不能为空"
    
    if not keyword_content or not keyword_content.strip():
        return "错误：keyword内容不能为空"
    
    from src.service.indexService import DRAFT_DIR
    import json
    
    keyword_data_dir = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "data")
    if not os.path.exists(keyword_data_dir):
        os.makedirs(keyword_data_dir)
    
    keyword_json_path = os.path.join(keyword_data_dir, "keyword.json")
    
    try:
        keyword_obj = json.loads(keyword_content)
        with open(keyword_json_path, 'w', encoding='utf-8') as f:
            json.dump(keyword_obj, f, ensure_ascii=False, indent=2)
        return f"成功保存keyword到: {keyword_json_path}"
    except json.JSONDecodeError:
        return "错误：keyword内容必须是有效的JSON格式"


def handle_bgm_select(bgm_name):
    if not bgm_name:
        return None
    bgm_full_path = get_bgm_path(bgm_name)
    print(f"[DEBUG] 选择BGM: {bgm_name}, 路径: {bgm_full_path}, 存在: {os.path.exists(bgm_full_path)}")
    if os.path.exists(bgm_full_path):
        return bgm_full_path
    return None


def handle_generate_draft(topic, bgm_name):
    if not topic or not topic.strip():
        return "错误：主题不能为空"
    
    try:
        from src.autocut.autocut import autoCut
        print(f"[DEBUG] 生成草稿 - 主题: {topic}, BGM: {bgm_name}")
        cutter = autoCut(topic=topic.strip(), bgm=bgm_name or "落.mp3")
        result = cutter.general_draft()
        return f"成功生成草稿，主题：{topic}"
    except Exception as e:
        import traceback
        print(f"[DEBUG] 生成草稿失败: {traceback.format_exc()}")
        return f"生成草稿失败: {str(e)}"


def handle_extract_audio(topic):
    from src.service.indexService import DRAFT_DIR
    audio_path = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "audioAlg", "audio.mp3")
    print(f"[DEBUG] 生成音频 - 主题: {topic}, DRAFT_DIR: {DRAFT_DIR}, 输出路径: {audio_path}")
    
    result = extract_audio_from_video(topic)
    if result and not result.startswith("错误"):
        print(f"[DEBUG] 生成音频完成，文件存在: {os.path.exists(audio_path)}")
        return result, audio_path
    return result, None


with gr.Blocks(title="视频草稿生成工具") as demo:
    gr.Markdown("# 视频草稿生成工具")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## 左侧")
            
            topic_input = gr.Textbox(label="主题", placeholder="请输入视频主题")
            
            init_btn = gr.Button("初始化草稿", variant="primary")
            init_result = gr.Textbox(label="初始化结果", interactive=False)
            
            gr.Markdown("### 上传视频")
            video_upload = gr.File(label="上传视频 (.mp4)", file_types=[".mp4"])
            video_player = gr.Video(label="视频播放")
            extract_audio_btn = gr.Button("生成音频", variant="primary")
            
            audio_player = gr.Audio(label="配音播放")
            
        with gr.Column():
            gr.Markdown("## 中间")
            
            asr_btn = gr.Button("ASR解析", variant="primary")
            
            download_asr_btn = gr.Button("下载ASR")
            download_asr_file = gr.File(label="下载ASR文件")
            
            danmu_prompt = gr.Textbox(
                label="弹幕Prompt",
                placeholder="ASR解析结果将显示在这里",
                lines=5
            )
            
            keyword_text = gr.Textbox(
                label="Keyword",
                placeholder='{"keyword": ["关键词1", "关键词2"]}',
                lines=3
            )
            
            update_keyword_btn = gr.Button("更新keyword", variant="primary")
            
            cover_prompt = gr.Textbox(
                label="封面Prompt",
                placeholder="封面Prompt将显示在这里",
                lines=5,
                interactive=False
            )
            
        with gr.Column():
            gr.Markdown("## 右侧")
            
            bgm_select = gr.Dropdown(
                label="背景音频",
                choices=get_bgm_list()
            )
            bgm_player = gr.Audio(
                        label="背景音频播放",
                        type="filepath",
                        interactive=False,
                        show_label=False,
                        autoplay=True,
                        )
            
            generate_btn = gr.Button("生成草稿", variant="primary")
            generate_result = gr.Textbox(label="生成结果", interactive=False)
    
    init_btn.click(
        fn=handle_init_draft,
        inputs=[topic_input],
        outputs=[init_result, video_player, audio_player, download_asr_file]
    )
    
    video_upload.change(
        fn=handle_upload_video,
        inputs=[topic_input, video_upload],
        outputs=[init_result]
    )
    
    video_upload.change(
        fn=get_video_path,
        inputs=[topic_input],
        outputs=[video_player]
    )

    extract_audio_btn.click(
        fn=handle_extract_audio,
        inputs=[topic_input],
        outputs=[init_result, audio_player]
    )
    
    asr_btn.click(
        fn=handle_asr_parse,
        inputs=[topic_input, danmu_prompt],
        outputs=[danmu_prompt, cover_prompt]
    )
    
    download_asr_btn.click(
        fn=handle_download_asr,
        inputs=[topic_input],
        outputs=[download_asr_file]
    )
    
    update_keyword_btn.click(
        fn=handle_update_keyword,
        inputs=[topic_input, keyword_text],
        outputs=[init_result]
    )
    
    bgm_select.change(
        fn=handle_bgm_select,
        inputs=[bgm_select],
        outputs=[bgm_player]
    )
    
    generate_btn.click(
        fn=handle_generate_draft,
        inputs=[topic_input, bgm_select],
        outputs=[generate_result]
    )


if __name__ == "__main__":
    demo.launch(allowed_paths=[DRAFT_DIR])
