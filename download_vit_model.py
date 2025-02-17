from transformers import ViTForImageClassification,ViTImageProcessor
import torch

checkpoint_path = "google/vit-base-patch16-224"
save_path = "/mnt/c/Users/sreeja/torchserve/vit-inference-torchserve/model_dir"
inference_processor = ViTImageProcessor.from_pretrained(checkpoint_path)
inference_model = ViTForImageClassification.from_pretrained(checkpoint_path)

# for param_tensor in inference_model.state_dict():
#     print(param_tensor, "\t", inference_model.state_dict()[param_tensor].size())

torch.save(inference_model.state_dict(),f"{save_path}/pytorch_model.bin")
