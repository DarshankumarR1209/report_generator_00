
from PIL import Image
from transformers import pipeline

BLIP_BASE = "Salesforce/blip-image-captioning-base"
BLIP_FINETUNED = r"./.cache/trained_accident"

SELECTED_MODEL = BLIP_BASE

def run_inference(task: str, model: str = None, inputs = None, gen_kwargs = {}):
    return pipeline(task, model=model, model_kwargs=dict(cache_dir=".cache/"))(inputs, generate_kwargs=gen_kwargs)

def image2text(img_path: str):
    image = Image.open(img_path)
    gen_kwargs = {"max_length": 512, "num_beams": 4}

    results = run_inference(
        task="image-to-text",
        model=SELECTED_MODEL,
        inputs=image,
        gen_kwargs=gen_kwargs
    )
    print("Inference results '{}':".format(img_path), results)
    return results[0].get('generated_text', img_path)
