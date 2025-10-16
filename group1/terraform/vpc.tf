resource "aws_vpc" "poudlard_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "poudlard-vpc"
  }
}

resource "aws_subnet" "poudlard_subnet" {
  vpc_id            = aws_vpc.poudlard_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  tags = {
    Name = "poudlard-subnet"
  }
}

resource "aws_security_group" "poudlard_sg" {
  name        = "poudlard-sg"
  description = "Allow HTTP/HTTPS/SSH"
  vpc_id      = aws_vpc.poudlard_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
