# SNS Topic for Alarm Notifications
resource "aws_sns_topic" "alarm_notifications" {
  name = "sqs-cloudwatch-alarm-topic"
}

# SNS Subscription for Email Notifications
resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.alarm_notifications.arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# CloudWatch Alarm for ApproximateAgeOfOldestMessage
resource "aws_cloudwatch_metric_alarm" "sqs_approximate_age_alarm" {
  alarm_name          = "SQSApproximateAgeTooHigh"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateAgeOfOldestMessage"
  namespace           = "AWS/SQS"
  period              = 60
  statistic           = "Maximum"
  threshold           = 300 # Alarm when the oldest message exceeds 5 minutes

  dimensions = {
    QueueName = var.sqs_queue_name
  }

  alarm_description = "Triggered when the ApproximateAgeOfOldestMessage in the SQS queue exceeds 5 minutes."
  actions_enabled   = true

  alarm_actions = [aws_sns_topic.alarm_notifications.arn]
}
