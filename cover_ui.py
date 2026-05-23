import gradio as gr
from pathlib import Path
import src.cover.cover as cover


def get_templates_list():
    base_cover_dir = Path("material/baseCover")
    if not base_cover_dir.exists():
        return ["请先将封面模板添加到 material/baseCover 目录"]
    folders = [d.name for d in base_cover_dir.iterdir() if d.is_dir()]
    if not folders:
        return ["请先在 material/baseCover 目录下创建模板文件夹"]
    return folders


def get_template_images(folder_name):
    if not folder_name or folder_name.startswith("请先"):
        return None, None

    base_dir = Path("material/baseCover") / folder_name
    vertical_path = base_dir / "vertical.png"
    horizontal_path = base_dir / "horizontal.png"

    v_path = str(vertical_path) if vertical_path.exists() else None
    h_path = str(horizontal_path) if horizontal_path.exists() else None

    return v_path, h_path


def get_fonts_list():
    fonts_dir = Path("material/fonts")
    if not fonts_dir.exists():
        return ["请先将字体文件添加到 material/fonts 目录"]
    fonts = list(fonts_dir.glob("*.ttf"))
    if not fonts:
        return ["material/fonts 目录下未找到 ttf 字体文件"]
    return [f.stem for f in fonts]


def get_font_path(font_name):
    if not font_name or font_name.startswith("请先") or font_name.startswith("未找到"):
        return None
    font_path = Path(f"material/fonts/{font_name}.ttf")
    if font_path.exists():
        return str(font_path)
    return None


def generate_cover_vertical(
    template_folder,
    font_name,
    text1, color1, font_size1,
    text2, color2, font_size2,
    text3, color3, font_size3,
    pos1_x, pos1_y,
    pos2_x, pos2_y,
    pos3_x, pos3_y,
    line_spacing,
    char_spacing1,
    char_spacing2,
    char_spacing3
):
    if not template_folder or template_folder.startswith("请先"):
        return None, "请先选择封面模板"

    template_path = f"material/baseCover/{template_folder}/vertical.png"
    if not Path(template_path).exists():
        return None, f"模板文件不存在: {template_path}"

    font_path = get_font_path(font_name)

    texts = [str(t) for t in [text1, text2, text3] if t and str(t).strip()]
    colors = [color1, color2, color3]
    font_sizes = [font_size1, font_size2, font_size3]
    positions = [(pos1_x, pos1_y), (pos2_x, pos2_y), (pos3_x, pos3_y)]
    char_spacing = [char_spacing1, char_spacing2, char_spacing3]

    valid_texts = [t.strip() for t in texts if t and t.strip()]
    if not valid_texts:
        return None, "请至少输入一行文字内容"

    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"catch/cover/generated_cover_{timestamp}.png"

    try:
        text_orientations = ["horizontal", "vertical", "horizontal"]
        cover.add_text_to_cover(
            template_path=template_path,
            output_path=output_path,
            texts=texts,
            colors=colors,
            font_sizes=font_sizes,
            line_spacing=line_spacing,
            custom_font_path=font_path,
            positions=positions,
            is_horizontal=False,
            text_orientations=text_orientations,
            char_spacing=char_spacing
        )
        return output_path, f"生成成功！文件已保存至: {output_path}"
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None, f"生成失败: {str(e)}"


def generate_cover_horizontal(
    template_folder,
    font_name,
    text1, color1, font_size1,
    text2, color2, font_size2,
    text3, color3, font_size3,
    pos1_x, pos1_y,
    pos2_x, pos2_y,
    pos3_x, pos3_y,
    line_spacing,
    char_spacing1,
    char_spacing2,
    char_spacing3
):
    if not template_folder or template_folder.startswith("请先"):
        return None, "请先选择封面模板"

    template_path = f"material/baseCover/{template_folder}/horizontal.png"
    if not Path(template_path).exists():
        return None, f"模板文件不存在: {template_path}"

    font_path = get_font_path(font_name)

    texts = [str(t) for t in [text1, text2, text3] if t and str(t).strip()]
    colors = [color1, color2, color3]
    font_sizes = [font_size1, font_size2, font_size3]
    positions = [(pos1_x, pos1_y), (pos2_x, pos2_y), (pos3_x, pos3_y)]
    char_spacing = [char_spacing1, char_spacing2, char_spacing3]

    valid_texts = [t.strip() for t in texts if t and t.strip()]
    if not valid_texts:
        return None, "请至少输入一行文字内容"

    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"catch/cover/generated_cover_{timestamp}.png"

    try:
        text_orientations = ["vertical", "vertical", "vertical"]
        cover.add_text_to_cover(
            template_path=template_path,
            output_path=output_path,
            texts=texts,
            colors=colors,
            font_sizes=font_sizes,
            line_spacing=line_spacing,
            custom_font_path=font_path,
            positions=positions,
            is_horizontal=True,
            text_orientations=text_orientations,
            char_spacing=char_spacing
        )
        return output_path, f"生成成功！文件已保存至: {output_path}"
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None, f"生成失败: {str(e)}"


def create_ui():
    with gr.Blocks(title="封面文字生成器") as demo:
        gr.Markdown("# 封面文字生成器")

        templates = get_templates_list()
        fonts = get_fonts_list()

        with gr.Row():
            font_dropdown = gr.Dropdown(
                choices=fonts,
                label="选择字体",
                value=fonts[0] if fonts else None
            )
            templates = get_templates_list()
            template_dropdown = gr.Dropdown(
                choices=templates,
                label="选择模板",
                value=templates[0] if templates else None
            )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 共同文字")

                main_title = gr.Textbox(
                    label="主标题",
                    placeholder="请输入主标题...",
                    value="为陈同甫赋壮词以寄之",
                    lines=1
                )

                sub_title = gr.Textbox(
                    label="副标题",
                    placeholder="请输入副标题...",
                    value="破阵子",
                    lines=1
                )

                description = gr.Textbox(
                    label="描述",
                    placeholder="请输入描述...",
                    value="醉里挑灯看剑，梦回吹角连营",
                    lines=1
                )

        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("## 竖版文字设置")

                with gr.Row():
                    v_color1 = gr.ColorPicker(
                        label="主标题文字颜色",
                        value="#0D131A",
                        scale=2
                    )

                with gr.Row():
                    v_font_size1 = gr.Slider(
                        minimum=24,
                        maximum=240,
                        value=92,
                        step=1,
                        label="主标题字体大小"
                    )

                with gr.Row():
                    v_char_spacing1 = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=0,
                        step=1,
                        label="主标题字间距"
                    )

                with gr.Row():
                    v_pos1_x = gr.Slider(
                        minimum=0,
                        maximum=2000,
                        value=42,
                        step=1,
                        label="主标题X坐标"
                    )
                    v_pos1_y = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        value=970,
                        step=1,
                        label="主标题Y坐标"
                    )

                with gr.Row():
                    v_color2 = gr.ColorPicker(
                        label="副标题文字颜色",
                        value="#0D131A",
                        scale=2
                    )

                with gr.Row():
                    v_font_size2 = gr.Slider(
                        minimum=24,
                        maximum=240,
                        value=185,
                        step=1,
                        label="副标题字体大小"
                    )

                with gr.Row():
                    v_char_spacing2 = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=40,
                        step=1,
                        label="副标题字间距"
                    )

                with gr.Row():
                    v_pos2_x = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        value=318,
                        step=1,
                        label="副标题X坐标"
                    )
                    v_pos2_y = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        value=59,
                        step=1,
                        label="副标题Y坐标"
                    )

                with gr.Row():
                    v_color3 = gr.ColorPicker(
                        label="描述文字颜色",
                        value="#fdd000",
                        scale=2
                    )

                with gr.Row():
                    v_font_size3 = gr.Slider(
                        minimum=24,
                        maximum=240,
                        value=67,
                        step=1,
                        label="描述字体大小"
                    )

                with gr.Row():
                    v_char_spacing3 = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=0,
                        step=1,
                        label="描述字间距"
                    )

                with gr.Row():
                    v_pos3_x = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        value=47,
                        step=1,
                        label="描述X坐标"
                    )
                    v_pos3_y = gr.Slider(
                        minimum=0,
                        maximum=2000,
                        value=1120,
                        step=1,
                        label="描述Y坐标"
                    )

                v_line_spacing_slider = gr.Slider(
                    minimum=0,
                    maximum=60,
                    value=0,
                    step=1,
                    label="行距"
                )

                v_generate_btn = gr.Button("生成竖版封面", variant="primary")

            with gr.Column(scale=3):
                gr.Markdown("## 生成结果")

                v_result_image = gr.Image(
                    label="生成的封面",
                    show_label=False,
                    type="filepath",
                    interactive=False
                )

                v_status_message = gr.Textbox(
                    label="状态信息",
                    interactive=False,
                    lines=2
                )

                v_generate_btn.click(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                main_title.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                sub_title.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                description.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_color1.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_color2.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_color3.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_font_size1.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_font_size2.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_font_size3.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_pos1_x.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_pos1_y.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_pos2_x.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_pos2_y.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_pos3_x.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_pos3_y.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_line_spacing_slider.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_char_spacing1.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_char_spacing2.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                v_char_spacing3.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

                template_dropdown.change(
                    fn=generate_cover_vertical,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, v_color1, v_font_size1,
                        sub_title, v_color2, v_font_size2,
                        description, v_color3, v_font_size3,
                        v_pos1_x, v_pos1_y,
                        v_pos2_x, v_pos2_y,
                        v_pos3_x, v_pos3_y,
                        v_line_spacing_slider,
                        v_char_spacing1, v_char_spacing2, v_char_spacing3
                    ],
                    outputs=[v_result_image, v_status_message]
                )

            with gr.Column(scale=2):
                gr.Markdown("## 横版文字设置")

                with gr.Row():
                    h_color1 = gr.ColorPicker(
                        label="主标题文字颜色",
                        value="#0D131A",
                        scale=2
                    )

                with gr.Row():
                    h_font_size1 = gr.Slider(
                        minimum=24,
                        maximum=240,
                        value=82,
                        step=1,
                        label="主标题字体大小"
                    )

                with gr.Row():
                    h_char_spacing1 = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=18,
                        step=1,
                        label="主标题字间距"
                    )

                with gr.Row():
                    h_pos1_x = gr.Slider(
                        minimum=0,
                        maximum=2000,
                        value=395,
                        step=1,
                        label="主标题X坐标"
                    )
                    h_pos1_y = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        value=40,
                        step=1,
                        label="主标题Y坐标"
                    )

                with gr.Row():
                    h_color2 = gr.ColorPicker(
                        label="副标题文字颜色",
                        value="#0D131A",
                        scale=2
                    )

                with gr.Row():
                    h_font_size2 = gr.Slider(
                        minimum=24,
                        maximum=240,
                        value=185,
                        step=1,
                        label="副标题字体大小"
                    )

                with gr.Row():
                    h_char_spacing2 = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=40,
                        step=1,
                        label="副标题字间距"
                    )

                with gr.Row():
                    h_pos2_x = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        value=698,
                        step=1,
                        label="副标题X坐标"
                    )
                    h_pos2_y = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        value=70,
                        step=1,
                        label="副标题Y坐标"
                    )

                with gr.Row():
                    h_color3 = gr.ColorPicker(
                        label="描述文字颜色",
                        value="#fdd000",
                        scale=2
                    )

                with gr.Row():
                    h_font_size3 = gr.Slider(
                        minimum=24,
                        maximum=240,
                        value=75,
                        step=1,
                        label="描述字体大小"
                    )

                with gr.Row():
                    h_char_spacing3 = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=0,
                        step=1,
                        label="描述字间距"
                    )

                with gr.Row():
                    h_pos3_x = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        value=237,
                        step=1,
                        label="描述X坐标"
                    )
                    h_pos3_y = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        value=44,
                        step=1,
                        label="描述Y坐标"
                    )

                h_line_spacing_slider = gr.Slider(
                    minimum=0,
                    maximum=60,
                    value=0,
                    step=1,
                    label="行距"
                )

                h_generate_btn = gr.Button("生成横版封面", variant="primary")

            with gr.Column(scale=3):
                gr.Markdown("## 生成结果")

                h_result_image = gr.Image(
                    label="生成的封面",
                    show_label=False,
                    type="filepath",
                    interactive=False
                )

                h_status_message = gr.Textbox(
                    label="状态信息",
                    interactive=False,
                    lines=2
                )

                template_dropdown.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_generate_btn.click(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                main_title.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                sub_title.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                description.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_color1.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_color2.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_color3.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_font_size1.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_font_size2.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_font_size3.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_pos1_x.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_pos1_y.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_pos2_x.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_pos2_y.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_pos3_x.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_pos3_y.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_line_spacing_slider.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_char_spacing1.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_char_spacing2.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

                h_char_spacing3.change(
                    fn=generate_cover_horizontal,
                    inputs=[
                        template_dropdown,
                        font_dropdown,
                        main_title, h_color1, h_font_size1,
                        sub_title, h_color2, h_font_size2,
                        description, h_color3, h_font_size3,
                        h_pos1_x, h_pos1_y,
                        h_pos2_x, h_pos2_y,
                        h_pos3_x, h_pos3_y,
                        h_line_spacing_slider,
                        h_char_spacing1, h_char_spacing2, h_char_spacing3
                    ],
                    outputs=[h_result_image, h_status_message]
                )

    return demo


if __name__ == "__main__":
    ui = create_ui()
    ui.launch(server_name="0.0.0.0", server_port=9001)
