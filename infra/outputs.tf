output "model_bucket_arn" {
  description = "ARN of the MLFlow Model Bucket"
  value       = aws_s3_bucket.model_bucket.arn
}

output "input_stream_arn" {
  value = module.source_kinesis_stream.stream_arn
}

output "output_stream_arn" {
  value = module.output_kinesis_stream.stream_arn
}
