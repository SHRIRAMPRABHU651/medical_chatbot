import gradio as gr
import google.generativeai as genai
from time import time
import PyPDF2
import io

# Set your Gemini API key
genai.configure(api_key="AIzaSyADul5IZjW7U9XR26VLYeItcn0vaUvjx9Q")

# Create the model - using flash for fastest responses
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Hardcoded PDF path and content extraction
PDF_PATH = "general symptoms.pdf"
pdf_content = extract_text_from_pdf(PDF_PATH)

# Custom CSS for modern medical UI
custom_css = """
body, html {
    margin: 0;
    padding: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background-color: #f0f4f8;
}

.gradio-container {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

.gr-chat-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    max-width: 100%;
    padding: 0;
    margin: 0;
    height: 100%;
}

.gr-chat {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: white;
    border-radius: 0;
    box-shadow: none;
    overflow: hidden;
}

.gr-chat-header {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: black;
    padding: 20px;
    font-weight: 600;
    font-size: 1.3rem;
    text-align: center;
}

.gr-chat-messages {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    background-color: #f9fbfd;
}

.gr-chatbot, .gr-user {
    max-width: 75%;
    margin: 10px 0;
    padding: 14px 20px;
    border-radius: 20px;
    line-height: 1.5;
    font-size: 0.95rem;
    word-wrap: break-word;
}

.gr-chatbot {
    background-color: #e9f1f8;
    border: 1px solid #dbe5ec;
    align-self: flex-start;
}

.gr-user {
    background-color: #4fc1e9;
    color: white;
    align-self: flex-end;
}

.gr-textbox {
    border-radius: 24px !important;
    padding: 12px 20px !important;
    border: 1px solid #ccc !important;
    width: 100%;
}

.gr-button {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 12px 24px !important;
    font-weight: 500 !important;
    margin-top: 10px;
}

@media (max-width: 768px) {
    .gr-chatbot, .gr-user {
        max-width: 90%;
        font-size: 0.9rem;
    }

    .gr-chat-messages {
        padding: 16px;
    }

    .gr-chat-header {
        font-size: 1.1rem;
    }
}
"""

# Response generation with timing and PDF context
def gemini_respond(message, history, system_message, max_tokens, temperature, top_p):
    start_time = time()
    
    # Prepare the prompt with medical context from PDF
    prompt = f"""SYSTEM INSTRUCTIONS: {system_message}
    
MEDICAL REFERENCE CONTEXT (from PDF):
{pdf_content[:5000]}... [truncated for brevity]

Current Conversation:
{'\n'.join([f'{"User" if i%2==0 else "Doctor"}: {h}' for i, h in enumerate(history)])}

User: {message}
Doctor:"""
    
    # Stream the response for faster perceived performance
    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
        },
        stream=True
    )
    
    # Stream the response token by token for faster display
    partial_response = ""
    for chunk in response:
        partial_response += chunk.text
        yield partial_response
    
    end_time = time()
    print(f"Response generated in {end_time - start_time:.2f} seconds")

# Gradio interface
with gr.Blocks(css=custom_css, theme=gr.themes.Default()) as demo:
    with gr.Row(elem_classes=["gr-chat-container"]):
        with gr.Column(elem_classes=["gr-chat"]):
            chatbot = gr.ChatInterface(
                fn=gemini_respond,
                additional_inputs=[
                    gr.Textbox(
                        value=(
                            "You are a professional medical practitioner. Use the provided medical reference material "
                            "to help diagnose conditions. Follow these guidelines strictly:\n"
                            "1. Analyze the described symptoms carefully\n"
                            "2. Provide a likely diagnosis (marked as 'Possible Condition:')\n"
                            "3. List 2-3 other potential conditions from the differential diagnosis\n"
                            "4. Offer practical self-care recommendations\n"
                            "5. Suggest when to seek immediate medical attention\n"
                            "6. Always include disclaimer that this is not professional medical advice\n"
                            "\n"
                            "Keep responses concise (4-6 bullet points max), professional yet empathetic, "
                            "and evidence-based. Reference the PDF content when relevant."
                        ),
                        visible=False,
                        label="system_message",
                    ),
                    gr.Slider(100, 1024, value=300, step=1, visible=False, label="Max tokens"),
                    gr.Slider(0.1, 1.0, value=0.3, step=0.1, visible=False, label="Temperature"),
                    gr.Slider(0.1, 1.0, value=0.9, step=0.05, visible=False, label="Top-p"),
                ],
                examples=[
                    ["I have fever (101°F), headache and body aches"],
                    ["Feeling nauseous after eating, with mild stomach pain"],
                    ["Persistent cough for 3 weeks, sometimes with phlegm"],
                    ["Sharp chest pain when breathing deeply"]
                ],
                title="Medical Diagnosis Assistant 🩺",
                description="Describe your symptoms for a preliminary assessment based on medical guidelines",
            )

if __name__ == "__main__":
    demo.launch()
