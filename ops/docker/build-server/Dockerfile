FROM nikolaik/python-nodejs:python3.10-nodejs14

# Install Docker
RUN apt-get update \
    && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    lsb-release \
    dumb-init

# This is to get rid of an annoying warning from apt-key below
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose

# Install Terraform
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
RUN apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
RUN apt-get update && apt-get install -y \
    terraform=1.0.1 \
    jq

# Install AWS CLI
RUN pip3 install -U awscli

# Install Checkov for Terraform security audits
RUN pip3 install checkov
RUN export PATH=/home/builder/.local/bin:$PATH

# Create user and group
RUN addgroup --system builder \
    && adduser --system --ingroup builder builder

# Setup Startup Script
COPY ./bootstrap.sh /bootstrap
RUN sed -i 's/\r$//g' /bootstrap
RUN chmod +x /bootstrap
RUN chown builder /bootstrap

COPY ./sleep.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown builder /start

COPY --chown=builder:builder . /app

USER builder

WORKDIR /app

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["bash", "-c", "/bootstrap && /start"]
