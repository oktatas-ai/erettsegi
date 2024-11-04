from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


def generate_alt_text(image):
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    alt_text = processor.decode(out[0], skip_special_tokens=True)

    return alt_text
