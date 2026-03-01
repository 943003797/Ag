import os
import json
import shutil
from dotenv import load_dotenv
from src.ai_models.ali_model.audio import get_transcription_by_audio
from src.ai_models.big_model.llm import LLM

load_dotenv()

SERVICE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SERVICE_DIR))
DRAFT_DIR = os.getenv("DRAFT_DIR", os.path.join(BASE_DIR, "drafts"))
BASE_DRAFT_PATH = os.path.join(BASE_DIR, "material", "baseDraft")
BGM_DIR = os.path.join(BASE_DIR, "material", "bgm")


def copy_base_draft(topic: str) -> str:
    """
    复制基础草稿模板到drafts目录下以主题命名的子目录
    
    Args:
        topic (str): 主题名称
        
    Returns:
        str: 成功消息或错误信息
    """
    if not topic or not topic.strip():
        return "错误：主题不能为空"
    
    target_dir = os.path.join(DRAFT_DIR, topic.strip())
    
    if os.path.exists(target_dir):
        return f"草稿目录已存在: {target_dir}"
    
    try:
        shutil.copytree(BASE_DRAFT_PATH, target_dir)
        return f"成功创建草稿目录: {target_dir}"
    except Exception as e:
        return f"创建草稿目录失败: {str(e)}"


def upload_video(topic: str, video_file: "File") -> str:
    """
    上传视频文件到草稿目录
    
    Args:
        topic (str): 主题名称
        video_file: 上传的视频文件
        
    Returns:
        str: 成功消息或错误信息
    """
    if not topic or not topic.strip():
        return "错误：主题不能为空"
    
    if video_file is None:
        return "错误：未选择视频文件"
    
    topic_dir = os.path.join(DRAFT_DIR, topic.strip())
    video_dir = os.path.join(topic_dir, "Resources", "videoAlg")
    
    if not os.path.exists(video_dir):
        return f"错误：草稿目录不存在，请先初始化草稿"
    
    target_path = os.path.join(video_dir, "video.mp4")
    
    try:
        shutil.copy(video_file, target_path)
        return f"成功上传视频: {target_path}"
    except Exception as e:
        return f"上传视频失败: {str(e)}"


def upload_audio(topic: str, audio_file: "File") -> str:
    """
    上传配音文件到草稿目录
    
    Args:
        topic (str): 主题名称
        audio_file: 上传的配音文件
        
    Returns:
        str: 成功消息或错误信息
    """
    if not topic or not topic.strip():
        return "错误：主题不能为空"
    
    if audio_file is None:
        return "错误：未选择配音文件"
    
    topic_dir = os.path.join(DRAFT_DIR, topic.strip())
    audio_dir = os.path.join(topic_dir, "Resources", "audioAlg")
    
    if not os.path.exists(audio_dir):
        return f"错误：草稿目录不存在，请先初始化草稿"
    
    target_path = os.path.join(audio_dir, "audio.mp3")
    
    try:
        shutil.copy(audio_file, target_path)
        return f"成功上传配音: {target_path}"
    except Exception as e:
        return f"上传配音失败: {str(e)}"


def asr_transcribe(topic: str) -> str:
    """
    对视频进行ASR语音识别
    
    Args:
        topic (str): 主题名称
        
    Returns:
        str: 转录文本或错误信息
    """
    if not topic or not topic.strip():
        return "错误：主题不能为空"
    
    topic_dir = os.path.join(DRAFT_DIR, topic.strip())
    audio_path = os.path.join(topic_dir, "Resources", "audioAlg", "audio.mp3")
    
    if not os.path.exists(audio_path):
        return "错误：配音文件不存在，请先生成音频"
    
    try:
        print(f"[DEBUG] ASR音频路径: {audio_path}")
        result = get_transcription_by_audio(audio_path)
        print(f"[DEBUG] ASR结果: {result}")
        
        text = ""
        sentences = []
        if "transcripts" in result:
            text = str(result["transcripts"][0])
        if "sentences" in result:
            sentences = result["sentences"]
        
        if text or sentences:
            asr_data_dir = os.path.join(topic_dir, "Resources", "data")
            if not os.path.exists(asr_data_dir):
                os.makedirs(asr_data_dir)
            asr_json_path = os.path.join(asr_data_dir, "asr.json")
            with open(asr_json_path, 'w', encoding='utf-8') as f:
                json.dump({"text": text, "sentences": sentences}, f, ensure_ascii=False, indent=2)
            print(f"[DEBUG] ASR结果已保存到: {asr_json_path}")
            return text
        else:
            print(f"[DEBUG] ASR返回结果: {result}")
            return "未能识别到语音内容"
    except Exception as e:
        import traceback
        print(f"[DEBUG] ASR解析失败: {traceback.format_exc()}")
        return f"ASR解析失败: {str(e)}"


def get_cover_prompt_from_llm(topic: str) -> str:
    """
    使用LLM根据主题生成封面图片的Prompt
    
    Args:
        topic (str): 主题名称
        
    Returns:
        str: 封面Prompt或错误信息
    """
    if not topic or not topic.strip():
        return "错误：主题不能为空"
    
    try:
        llm = LLM()
        return llm.get_cover_prompt(topic)
    except Exception as e:
        return f"生成封面Prompt失败: {str(e)}"


def get_bgm_list():
    """
    获取背景音频列表
    
    Returns:
        list: 背景音频文件名列表
    """
    print(f"[DEBUG] BGM_DIR: {BGM_DIR}")
    if not os.path.exists(BGM_DIR):
        print(f"[DEBUG] BGM目录不存在: {BGM_DIR}")
        return []
    
    bgm_files = []
    for file in os.listdir(BGM_DIR):
        if file.lower().endswith(('.mp3', '.mp4', '.wav', '.aac', '.m4a', '.flac')):
            bgm_files.append(file)
    
    print(f"[DEBUG] BGM文件列表: {bgm_files}")
    return sorted(bgm_files)


def get_audio_path(topic: str):
    """获取草稿目录中配音文件的路径"""
    if not topic or not topic.strip():
        return None
    audio_path = os.path.join(DRAFT_DIR, topic.strip(), "Resources", "audioAlg", "audio.mp3")
    if os.path.exists(audio_path):
        return audio_path
    return None
    
    return sorted(bgm_files)


def get_bgm_path(bgm_name: str) -> str:
    """
    获取背景音频的完整路径
    
    Args:
        bgm_name (str): 背景音频文件名
        
    Returns:
        str: 背景音频完整路径
    """
    if not bgm_name:
        return ""
    
    return os.path.join(BGM_DIR, bgm_name)


def extract_audio_from_video(topic: str) -> str:
    """
    从视频中提取音频并保存到草稿目录
    
    Args:
        topic (str): 主题名称
        
    Returns:
        str: 成功消息或错误信息
    """
    if not topic or not topic.strip():
        return "错误：主题不能为空"
    
    topic_dir = os.path.join(DRAFT_DIR, topic.strip())
    video_path = os.path.join(topic_dir, "Resources", "videoAlg", "video.mp4")
    audio_dir = os.path.join(topic_dir, "Resources", "audioAlg")
    
    if not os.path.exists(video_path):
        return "错误：视频文件不存在，请先上传视频"
    
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    
    audio_path = os.path.join(audio_dir, "audio.mp3")
    
    try:
        try:
            from moviepy.editor import VideoFileClip
        except ImportError:
            from moviepy import VideoFileClip
        print(f"[DEBUG] 视频路径: {video_path}")
        print(f"[DEBUG] 音频输出路径: {audio_path}")
        video = VideoFileClip(video_path)
        print(f"[DEBUG] 视频音频: {video.audio}")
        if video.audio is None:
            return "错误：视频中没有音频轨道"
        video.audio.write_audiofile(audio_path, codec='libmp3lame')
        video.close()
        return f"成功提取音频: {audio_path}"
    except Exception as e:
        import traceback
        print(f"[DEBUG] 提取音频失败: {traceback.format_exc()}")
        return f"提取音频失败: {str(e)}"
