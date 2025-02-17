import logging
import os
import io
import torch
from PIL import Image
from transformers import ViTImageProcessor, ViTForImageClassification
from ts.torch_handler.base_handler import BaseHandler
import sys

logging.basicConfig(stream=sys.stdout, format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__file__)

class ViTHandler(BaseHandler):
    """
    Vision Transformer handler for image classification using TorchServe.
    """

    def __init__(self):
        super(ViTHandler, self).__init__()
        self.initialized = False

    def initialize(self, ctx):
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_dir = properties.get("model_dir")  # Fixed model directory retrieval

        # Select device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

        # Load model and processor
        self.processor = ViTImageProcessor.from_pretrained(model_dir, local_files_only=True)
        self.model = ViTForImageClassification.from_pretrained(model_dir, local_files_only=True)
        self.model.to(self.device)
        self.model.eval()

        logger.info(f"Model loaded from {model_dir} on {self.device}")
        self.initialized = True

    def preprocess(self, data):
        """ Convert input bytes into a format suitable for model inference. """
        images = []
        for row in data:
            image = row.get("data") or row.get("body") or row.get("file")
            if isinstance(image, (bytearray, bytes)):
                image = Image.open(io.BytesIO(image))
                images.append(image)

        if not images:
            raise ValueError("No valid images found in the input data.")

        inputs = self.processor(images=images, return_tensors="pt")
        for key in inputs:
            inputs[key] = inputs[key].to(self.device)  # Move tensors to the correct device
        
        return inputs

    def inference(self, inputs):
        """ Perform inference on the model. """
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = outputs.logits.argmax(-1)
        return predictions

    def postprocess(self, inference_output):
        """ Convert predictions into human-readable labels. """
        return [{"label": self.model.config.id2label[idx.item()]} for idx in inference_output]

    def handle(self, data, context):
        """ Main TorchServe handler function. """
        if not self.initialized:
            self.initialize(context)

        if not data:
            return []

        processed_data = self.preprocess(data)
        predictions = self.inference(processed_data)
        return self.postprocess(predictions)
