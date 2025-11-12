import os
import logging
from typing import Optional, Dict, Any, List

import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering


class MultimodalAgent:
    def __init__(self, device: Optional[str] = None, log_path: str = "logs/agent.log") -> None:
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.logger = logging.getLogger("multimodal_agent")
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            fh = logging.FileHandler(log_path, encoding="utf-8")
            fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)
        self.caption_processor = None
        self.caption_model = None
        self.vqa_processor = None
        self.vqa_model = None

    def _load_captioner(self) -> None:
        if self.caption_model is None:
            self.caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.caption_model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            ).to(self.device).eval()

    def _load_vqa(self) -> None:
        if self.vqa_model is None:
            self.vqa_processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
            self.vqa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base").to(self.device).eval()

    def caption(self, image: Image.Image, max_new_tokens: int = 30, num_beams: int = 3) -> str:
        self._load_captioner()
        inputs = self.caption_processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            out = self.caption_model.generate(**inputs, max_new_tokens=max_new_tokens, num_beams=num_beams)
        return self.caption_processor.decode(out[0], skip_special_tokens=True)

    def vqa(self, image: Image.Image, question: str, max_new_tokens: int = 20, num_beams: int = 1) -> str:
        self._load_vqa()
        inputs = self.vqa_processor(images=image, text=question, return_tensors="pt").to(self.device)
        with torch.no_grad():
            out = self.vqa_model.generate(**inputs, max_new_tokens=max_new_tokens, num_beams=num_beams)
        return self.vqa_processor.decode(out[0], skip_special_tokens=True)

    def _route(self, prompt: Optional[str]) -> str:
        if not prompt or prompt.strip() == "":
            return "caption"
        p = prompt.lower()
        if any(k in p for k in ["describe", "caption", "summary", "summarize", "what is in this image"]):
            return "caption"
        return "vqa"

    def run(self, image: Image.Image, prompt: Optional[str]) -> Dict[str, Any]:
        steps: List[str] = []
        mode = self._route(prompt)
        steps.append(f"route:{mode}")
        cap = self.caption(image)
        steps.append(f"caption:{cap}")
        if mode == "caption":
            answer = cap
        else:
            q = prompt.strip()
            answer = self.vqa(image, q)
            steps.append(f"vqa:{q}->{answer}")
        self.logger.info("mode=%s", mode)
        self.logger.info("caption=%s", cap)
        if mode != "caption":
            self.logger.info("question=%s answer=%s", prompt, answer)
        return {"mode": mode, "caption": cap, "answer": answer, "final_answer": answer, "steps": steps, "device": self.device}
