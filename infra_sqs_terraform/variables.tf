# Variables for existing resources

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "LambdaImage_generation_pro"
}

variable "sqs_queue_name" {
  description = "Name of the SQS queue"
  type        = string
  default     = "image_generation_pro"
}

variable "sqs_queue_arn" {
  description = "ARN of the SQS queue"
  type        = string
  default     = "arn:aws:sqs:eu-west-1:244530008913:image_generation_pro"
}

variable "notification_email" {
  description = "Email address for receiving notifications"
  type        = string
}
