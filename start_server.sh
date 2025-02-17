#!/bin/bash
torchserve --ts-config config.properties --foreground  --models vit-model=vit-model.mar --disable-token-auth --enable-model-api --ncs
#torchserve --ts-config config.properties --foreground --log-config log4j2.xml --models vit-model=vit-model.mar --disable-token-auth --enable-model-api --ncs
