output "instance_id" {
  value = aws_instance.poudlard.id
}

output "instance_public_ip" {
  value = aws_instance.poudlard.public_ip
}
