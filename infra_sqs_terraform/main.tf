# Ressurser

# Outputs
output "lambda_function_name" {
  description = "Navnet på Lambda-funksjonen"
  value       = "LambdaImage_generation_pro"
}

output "sqs_queue_url" {
  description = "URL til SQS-køen"
  value       = "https://sqs.eu-west-1.amazonaws.com/244530008913/image_generation_pro"
}

output "sqs_queue_arn" {
  description = "ARN til SQS-køen"
  value       = "arn:aws:sqs:eu-west-1:244530008913:image_generation_pro"
}
