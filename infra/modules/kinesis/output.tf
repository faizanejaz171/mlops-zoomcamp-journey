output "stream_arn" {
  value = aws_kinesis_stream.stream.arn
}

# Yeh naya block add karna hai
output "stream_name" {
  value = aws_kinesis_stream.stream.name
}
