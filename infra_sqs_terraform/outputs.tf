# Outputs
output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = var.lambda_function_name
}

output "sqs_queue_url" {
  description = "URL of the SQS queue"
  value       = "https://sqs.eu-west-1.amazonaws.com/244530008913/${var.sqs_queue_name}"
}

output "sqs_queue_arn" {
  description = "ARN of the SQS queue"
  value       = var.sqs_queue_arn
}

output "cloudwatch_alarm_name" {
  description = "Name of the CloudWatch alarm"
  value       = aws_cloudwatch_metric_alarm.sqs_approximate_age_alarm.alarm_name
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for notifications"
  value       = aws_sns_topic.alarm_notifications.arn
}
