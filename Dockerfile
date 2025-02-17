# Use pytorch/torchserve:latest as the base image
FROM pytorch/torchserve:latest
#FROM aruntiwary/vit_torchserve_image:v1
# Set the working directory inside the container
WORKDIR /vit

# Copy all files from the current directory to /app in the container
COPY . /vit
RUN  pip install --upgrade pip
RUN  pip install -r req.txt.min
# Expose the necessary ports
EXPOSE 9085 9086 9087 9070 9071

# Run the shell script to start the server
CMD ["sh", "start_server.sh"]
