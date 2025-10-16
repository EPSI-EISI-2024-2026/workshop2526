// Terraform placeholder - example AWS EC2 provisioning
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "eu-west-3"
}

resource "aws_instance" "poudlard" {
  ami           = "ami-xxxxxxxx" # Replace with valid AMI
  instance_type = "t3.medium"
  tags = {
    Name = "poudlard-node"
  }
  user_data = <<-EOF
              #!/bin/bash
              apt update && apt install -y docker.io docker-compose git
              cd /opt
              git clone https://github.com/your/repo.git /opt/poudlard || true
              cd /opt/poudlard/docker
              docker-compose up -d
              EOF
}

