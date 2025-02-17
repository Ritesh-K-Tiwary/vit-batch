#!/bin/bash
torch-model-archiver \
    --model-name vit-model \
    --version 1.0 \
    --serialized-file "model_dir/pytorch_model.bin" \
    --export-path model_store \
    --force \
    --handler "handler.py" \
    --extra-files "model_dir/config.json,model_dir/preprocessor_config.json"
