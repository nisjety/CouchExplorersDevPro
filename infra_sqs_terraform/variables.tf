# Variabler for eksisterende ressurser

variable "lambda_function_name" {
  description = "Navnet på Lambda-funksjonen"
  type        = string
  default     = "LambdaImage_generation_pro"
}

variable "sqs_queue_name" {
  description = "Navnet på SQS-køen"
  type        = string
  default     = "image_generation_pro"
}

variable "sqs_queue_arn" {
  description = "ARN til SQS-køen"
  type        = string
  default     = "arn:aws:sqs:eu-west-1:244530008913:image_generation_pro"
}
