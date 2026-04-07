# Prototyping tools

Chọn tool theo POC option của nhóm. Không cần dùng hết — chọn 1-2 tool quen nhất.

## Tool theo POC option

| Option | Tool | Mô tả | Link |
|---|---|---|---|
| **A — Prompt-based** | ChatGPT / Claude | Demo trực tiếp trong chat | chatgpt.com / claude.ai |
| **A — Prompt-based** | Streamlit | UI Python nhanh, 1 file | streamlit.io |
| **A — Prompt-based** | Gradio | UI cho ML demo | gradio.app |
| **A — Prompt-based** | Google Colab | Notebook online, free GPU | colab.research.google.com |
| **B — Mock flow** | Figma | Clickable prototype | figma.com |
| **B — Mock flow** | Canva | Mock screens nhanh | canva.com |
| **B — Mock flow** | Loom | Record walkthrough video | loom.com |
| **C — Working code** | Cursor | AI-assisted coding | cursor.com |
| **C — Working code** | v0 | Generate UI từ prompt | v0.dev |
| **C — Working code** | Replit | Online IDE, easy deploy | replit.com |

---

## Chi tiết từng tool

### Option A — Prompt-based

**ChatGPT / Claude:**
Cách nhanh nhất để demo AI product. Viết system prompt tốt, tạo custom GPT hoặc Claude Project, share link cho người xem thử. Phù hợp khi product chính là chatbot hoặc Q&A. Bắt đầu: vào ChatGPT → Explore GPTs → Create, hoặc Claude → Projects → New.

**Streamlit:**
Framework Python tạo web app từ 1 file. Kéo thả input, hiện output, deploy free trên Streamlit Cloud. Phù hợp khi cần UI đẹp hơn chat nhưng không muốn viết frontend. Bắt đầu: `pip install streamlit` → viết `app.py` → `streamlit run app.py`.

**Gradio:**
Tương tự Streamlit nhưng thiên về ML demo. Tự tạo input/output interface. Phù hợp khi demo model xử lý ảnh, text, audio. Bắt đầu: `pip install gradio` → dùng `gr.Interface()` wrap function.

**Google Colab:**
Jupyter notebook online, free GPU. Phù hợp khi cần chạy code nặng hoặc show notebook cho người khác. Bắt đầu: vào colab.research.google.com → New notebook → chạy cell.

### Option B — Mock flow

**Figma:**
Design tool tạo clickable prototype. Vẽ màn hình → nối flow → share link test. Phù hợp khi muốn show trải nghiệm user hoàn chỉnh mà chưa cần code. Bắt đầu: tạo account free → dùng template có sẵn.

**Canva:**
Tạo mock screens nhanh bằng drag-and-drop. Phù hợp khi cần poster, slides, hoặc mock UI đơn giản. Bắt đầu: chọn template "Mobile App" hoặc "Presentation".

**Loom:**
Record màn hình + giọng nói. Phù hợp khi demo flow phức tạp hoặc cần record backup phòng internet chết. Bắt đầu: cài extension Chrome → bấm record.

### Option C — Working code (bonus)

**Cursor:**
VS Code + AI coding assistant. Viết code nhanh hơn với AI autocomplete và chat. Phù hợp khi nhóm có dev experience. Bắt đầu: download → mở project → dùng Cmd+K để generate code.

**v0 (Vercel):**
Generate React UI từ text prompt. Paste mô tả → ra code chạy được. Phù hợp khi cần frontend đẹp mà không rành React. Bắt đầu: vào v0.dev → mô tả UI muốn tạo.

**Replit:**
Online IDE, code + deploy 1 chỗ. Phù hợp khi nhóm muốn code cùng lúc (multiplayer) hoặc cần deploy nhanh. Bắt đầu: tạo Repl → chọn template → code → bấm Run.

---

## Gợi ý chọn nhanh

- Chưa biết code → **Option B** (Figma/Canva) + 1 prompt test thật
- Biết Python cơ bản → **Option A** (Streamlit hoặc Colab)
- Dev experience → **Option C** (Cursor + Replit)
- Bất kể option nào: phải có **ít nhất 1 prompt/AI call chạy thật**
