
## VIT batch image

```sh
docker.io/sarthakd112/vit_torchserve_batch_image
git clone https://github.com/EliSchwartz/imagenet-sample-images.git images

## To Kill ports
lsof -i :7070
kill -9 <pid>
```

```sh
git clone https://github.com/KrArunT/vit-batch.git 
cd vit-batch

## Run following command

docker run --rm -it -d --name vit \
    -p 0.0.0.0:9085:9085 -p 0.0.0.0:9086:9086 \ 
    -p 0.0.0.0:9087:9087 -p 0.0.0.0:9070:9070  \
    -p 0.0.0.0:9071:9071  \
    -v ./config.properties:/home/model-server/config.properties  \
    aruntiwary/vit_torchserve_batch_image:v1 

## To run batch inference 
python infer_batch.py

```

