# 🩺 Medical Diagnosis Assistant Chatbot - README

## 📘 Project Overview

This project is a web-based **Medical Diagnosis Assistant** chatbot built using **Gradio**, powered by **Gemini 1.5 Flash** via Google's `generativeai` library. It leverages a **RAG (Retrieval-Augmented Generation)** approach by extracting medical knowledge from a local **PDF document** and using it to provide context-aware responses to symptom-related queries.

---

## 📌 Features

* Modern full-screen chat UI with responsive layout
* PDF-based context feeding (RAG method)
* Real-time streamed responses
* Gemini 1.5 Flash API integration
* Medical system prompt logic (diagnosis, self-care, disclaimer, etc.)
* Designed for professional and empathetic output

---

## 🏗️ Tech Stack

| Tool / Library       | Purpose                        |
| -------------------- | ------------------------------ |
| Gradio               | Frontend UI & chat interface   |
| Google Generative AI | Backend LLM (Gemini-1.5-flash) |
| PyPDF2               | PDF content extraction         |
| Python               | Core logic and integration     |

---

## 📂 Project Structure

```
medical_chatbot/
├── app.py                # Main Gradio app
├── general symptoms.pdf  # PDF file containing medical context
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🔄 How RAG (Retrieval-Augmented Generation) is Used

**RAG = Retrieval + Generation.**

In this project:

### 📥 1. Retrieval

* `PyPDF2` is used to load the medical reference document: `general symptoms.pdf`.
* The entire content (or first 5000 characters) is extracted and stored as `pdf_content`.

```python
PDF_PATH = "general symptoms.pdf"
pdf_content = extract_text_from_pdf(PDF_PATH)
```

### 🧠 2. Augmented Prompt Construction

* The PDF content is injected into the **system prompt**.
* The prompt also includes **conversation history** and the **user message**.

```python
prompt = f"""
SYSTEM INSTRUCTIONS: {system_message}

MEDICAL REFERENCE CONTEXT (from PDF):
{pdf_content[:5000]}... [truncated for brevity]

Current Conversation:
{history_formatted}

User: {message}
Doctor:"""
```

### 🗣️ 3. Generation

* This enriched prompt is sent to Gemini’s model (`gemini-1.5-flash`) using `generate_content`.
* Streaming is enabled for real-time interaction.

### 📊 Diagram

```
User Input -->
              +----------------+
              |     Prompt     |
              |  (History +    |
              |   PDF context) |
              +----------------+
                        |
                        v
                +--------------+
                |   Gemini AI  |
                +--------------+
                        |
              Streamed Response --> Gradio Chat UI
```

---

## 🖼️ UI Overview

### ✅ Desktop Layout

* Full-screen fluid chat interface
* Custom styling with modern padding, colors, rounded corners
* Sticky chat with examples pre-filled

### 📱 Mobile Responsive

* Optimized for smaller screens
* Adapts width and layout of user and chatbot messages

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/shriramprabhu651/medical-chatbot.git
cd medical-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your Gemini API Key

In `app.py`:

```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```

### 4. Launch the App

```bash
python app.py
```

App will be available at: `http://localhost:7860`

---

## 🔐 Disclaimer

This chatbot is for **informational and educational purposes only**. It does **not constitute professional medical advice**, diagnosis, or treatment. Always consult a licensed healthcare provider for real medical conditions.

---

## 📌 To-Do / Enhancements

* [ ] Upload PDF support
* [ ] Chat history persistence
* [ ] Dark/light mode toggle
* [ ] Voice input for accessibility

---

## 🧾 License

MIT License

---

## 🙌 Credits

* OpenAI & Google for LLM APIs
* Gradio team for rapid prototyping tools
* Medical content adapted from sample PDF
