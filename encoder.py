import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

MODEL_NAME = "openai/clip-vit-base-patch32"
device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading CLIP on", device)
model = CLIPModel.from_pretrained(MODEL_NAME).to(device).eval()
processor = CLIPProcessor.from_pretrained(MODEL_NAME)


def _to_tensor(out):
    """Different transformers versions return a tensor or an output object."""
    if isinstance(out, torch.Tensor):
        return out
    if hasattr(out, "pooler_output") and out.pooler_output is not None:
        return out.pooler_output
    return out[0]


def _normalize(feats):
    return feats / feats.norm(dim=-1, keepdim=True)


@torch.no_grad()
def encode_images(paths):
    images = []
    for p in paths:
        with Image.open(p) as im:
            images.append(im.convert("RGB"))
    inputs = processor(images=images, return_tensors="pt").to(device)
    feats = _to_tensor(model.get_image_features(**inputs))
    return _normalize(feats).cpu().numpy()


@torch.no_grad()
def encode_text(text):
    inputs = processor(text=[text], return_tensors="pt", padding=True).to(device)
    feats = _to_tensor(model.get_text_features(**inputs))
    return _normalize(feats)[0].cpu().numpy()