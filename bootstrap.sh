
#!/bin/bash

prepare_ubuntu() {
  sudo apt-get update
  sudo apt-get dist-upgrade -y
  sudo apt-get install -y --no-install-recommends \
    apt-transport-https \
    curl \
    gnupg-curl \
    htop \
    lsof \
    tree \
    tzdata \
    lsb-release \
    bzip2 \
    unzip \
    xz-utils
}

install_docker() {
  # Docker
  export CHANNEL=stable
  curl -fsSL https://get.docker.com/ | sh
  ## Add Docker daemon configuration
  cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "icc": false,
  "disable-legacy-registry": true,
  "userland-proxy": false,
  "live-restore": true
}
EOF
  ## Start docker service
  sudo systemctl enable docker
  sudo systemctl start docker
  ## Add current user to docker group
  sudo usermod -aG docker $USER

  ## show information
  docker version
  docker info

  # Docker Compose
  sudo curl -L https://github.com/docker/compose/releases/download/1.21.0-rc1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  ## show docker-compose version
  docker-compose version
}

provision_docker() {
  echo "Provisioning ..."
  prepare_ubuntu
  install_docker
  # Downlaod the Dockerfile and docker-compose.yml

}

provision_elk() {
  # Install JRE (Only needed for running PSI locally)
  cd logging
  docker-compose up -d
  docker-compose ps
}

build() {
  docker build -t openusm -f Dockerfile .
}

up() {
  local name=${1:-openusm}


  echo "Starting services for $name ..."


    docker-compose -p $name up -d
}

down() {
  local name=${1:-openusm}
  echo "Starting services for $name ..."
  docker-compose -p $name down
}

logs() {
#  local name=${1:-openusm}
#  shift
  cd logging
  echo "Logs for $name ..."
  docker-compose  logs $@
}



command=$1
shift
case "$command" in
  build)          build ;;
  up)             up $@ ;;
  down)           down $@ ;;
  logs)           logs $@ ;;
  provision_docker)      provision_docker $@ ;;
  provision_elk) provision_elk ;;
  *)        echo "Usage: <build|up|down|logs|psi|provision_docker|provision_elk>" ;;
esac
