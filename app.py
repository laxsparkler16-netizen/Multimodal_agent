import gradio as gr
from PIL import Image
from agent import MultimodalAgent

agent = MultimodalAgent()
#making changes

def infer(image: Image.Image, prompt: str):
    if image is None:
        return "Please upload an image.", {}
    res = agent.run(image, prompt or "")
    text = res["final_answer"]
    logs = {
        "mode": res["mode"],
        "caption": res["caption"],
        "answer": res["answer"],
        "steps": res["steps"],
        "device": res["device"],
    }
    return text, logs


with gr.Blocks() as demo:
    gr.Markdown("# Multimodal Agent\nUpload an image and enter a prompt.")
    with gr.Row():
        with gr.Column():
            img = gr.Image(type="pil", label="Image")
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="e.g., Describe the dashboard, What is the number in the top right?",
                lines=2,
            )
            btn = gr.Button("Run")
        with gr.Column():
            out_text = gr.Textbox(label="Agent Answer", lines=4)
            out_json = gr.JSON(label="Trace")
    btn.click(fn=infer, inputs=[img, prompt], outputs=[out_text, out_json])
    gr.Markdown(
        "Sample prompts:\n- Describe the image\n- What is the main issue in this UI?\n- How many bars are there?\n- What is the trend shown in the chart?"
    )


if __name__ == "__main__":
    demo.launch()
