---
title: AI Skin Detection Demo
emoji: 🩺
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---

# AI Skin Detection Demo

這是一個可部署到 Hugging Face Spaces 的 YOLOv8 皮膚狀況偵測示範專案。

## 功能

- 使用 Gradio Blocks 建立雙欄介面
- 左側上傳圖片（PIL）
- 右側顯示 YOLOv8 框選後結果
- 提供「開始偵測」與「清除」按鈕
- 頁面下方附使用提醒

## 專案結構

- `app.py`：Gradio 應用與 YOLOv8 推論邏輯
- `best.pt`：本地 YOLOv8 權重檔（請放在專案根目錄）
- `requirements.txt`：相依套件清單

## 本機執行

```bash
pip install -r requirements.txt
python app.py
```

啟動後預設可由 `http://127.0.0.1:7860` 開啟。

## 部署到 Hugging Face Spaces

1. 在 Hugging Face 建立新的 Space，選擇 **Gradio** SDK。
2. 上傳以下檔案到 Space 根目錄：
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `best.pt`
3. Space 會自動安裝套件並啟動。

## 重要提醒

此模型僅供教學展示，不作為醫療診斷依據。
