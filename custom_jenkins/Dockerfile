FROM jenkins/jenkins:lts

USER root

# Install prerequisites
RUN apt-get update -y &&     apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release &&     apt-get clean

# Add Docker's official GPG key
RUN install -m 0755 -d /etc/apt/keyrings &&     curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc &&     chmod a+r /etc/apt/keyrings/docker.asc

# Set up Docker repository (multi-architecture support)
RUN echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian   $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
RUN apt-get update -y &&     apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin &&     apt-get clean

# Add Jenkins user to docker group
RUN usermod -aG docker jenkins

USER jenkins
