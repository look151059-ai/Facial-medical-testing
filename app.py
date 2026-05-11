import os
from typing import Optional

import gradio as gr
from PIL import Image
from ultralytics import YOLO

# 只載入一次模型，避免每次點擊按鈕都重複初始化造成延遲
MODEL_PATH = "best.pt"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"找不到模型檔案：{MODEL_PATH}")

model = YOLO(MODEL_PATH)


def predict(image: Optional[Image.Image]) -> Optional[Image.Image]:
    """
    使用 YOLOv8 進行皮膚狀況偵測。

    Args:
        image: 由 Gradio 上傳的 PIL 圖片。

    Returns:
        框選後的 PIL 圖片；若無輸入則回傳 None。
    """
    if image is None:
        return None

    # 執行推論（PIL 可直接作為輸入）
    results = model.predict(source=image, verbose=False)

    # results[0].plot() 會回傳含框選與標籤的 BGR ndarray
    plotted_bgr = results[0].plot()

    # 轉成 RGB 再包裝回 PIL，才能正確顯示在 Gradio Image
    result_image = Image.fromarray(plotted_bgr[:, :, ::-1])
    return result_image


with gr.Blocks(title="AI Skin Detection Demo") as demo:
    gr.Markdown("# AI Skin Detection Demo")
    gr.Markdown(
        "上傳皮膚圖片後，點擊「開始偵測」，系統會使用 YOLOv8 模型標示可能的皮膚狀況區域。"
    )

    with gr.Row():
        with gr.Column():
            input_image = gr.Image(
                label="上傳圖片",
                type="pil",  # 確保輸入格式為 PIL
            )
        with gr.Column():
            output_image = gr.Image(
                label="偵測結果",
                type="pil",
            )

    with gr.Row():
        detect_btn = gr.Button("開始偵測", variant="primary")
        clear_btn = gr.Button("清除")

    # 綁定按鈕事件
    detect_btn.click(
        fn=predict,
        inputs=input_image,
        outputs=output_image,
    )

    # 清除輸入與輸出
    clear_btn.click(
        fn=lambda: (None, None),
        inputs=None,
        outputs=[input_image, output_image],
    )

    gr.Markdown("---")
    gr.Markdown("**使用提醒：此模型僅供教學展示，不作為醫療診斷。**")


if __name__ == "__main__":
    # 在 Spaces 使用 0.0.0.0，本機使用 127.0.0.1，避免本機瀏覽器連到無效位址
    is_hf_spaces = os.getenv("SPACE_ID") is not None
    server_name = "0.0.0.0" if is_hf_spaces else "127.0.0.1"
    server_port = int(os.getenv("PORT", 7860))
    demo.launch(server_name=server_name, server_port=server_port)
