#!/bin/bash

# Caminho para a pasta do repositório Git
REPO_DIR="/home/jcurvelo/diarias-back"

# Caminho para a pasta do docker-compose.yml
DOCKER_COMPOSE_DIR="/home/jcurvelo/diarias"

# Nome da imagem e do container Docker
IMAGE_NAME="diarias_python-back"
CONTAINER_NAME="diarias-backend"

# Função para realizar git pull
git_pull() {
    echo "Atualizando o repositório Git na pasta $REPO_DIR"
    cd "$REPO_DIR" || exit
    git pull
}

# Função para remover a imagem Docker
remove_image() {
    echo "Removendo a imagem Docker $IMAGE_NAME"
    sudo docker rmi "$IMAGE_NAME" -f
}

# Função para remover o container Docker
remove_container() {
    echo "Removendo o container Docker $CONTAINER_NAME"
    sudo docker rm "$CONTAINER_NAME" -f
}

# Função para iniciar o docker-compose
start_docker_compose() {
    echo "Iniciando o docker-compose"
    cd "$DOCKER_COMPOSE_DIR" || exit
    sudo docker-compose up -d
}

# Executando as funções
git_pull
remove_container
remove_image
start_docker_compose

echo "Script concluído com sucesso!"
