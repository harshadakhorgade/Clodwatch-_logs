# Clodwatch-_logs



 **Django deployment on AWS Elastic Beanstalk with CloudWatch logging, S3 static file handling, and Secrets Manager** integration.

> ⚠️ **Important Security Note**: This version includes secrets you mentioned. **Do not publish this README publicly or push it to GitHub with real secrets.** You should always use environment variables or `.env` files excluded via `.gitignore`.

---

## 🌐 Django Project Deployment on AWS Elastic Beanstalk with CloudWatch, S3, and Secrets Manager

This guide documents how to deploy a Django application on AWS Elastic Beanstalk, configure CloudWatch logging via Watchtower, store sensitive data using Secrets Manager, and use Amazon S3 and CloudFront for static files.

---

### 🔐 AWS Secrets Manager Configuration

**Secret Name**: `django_app_secrets`

```json
{
  "SECRET_KEY": "j6#7b5h!*01q7%61k6&#c)*we99$h5ezrjvtox562v87^yhfr#",
  "AWS_ACCESS_KEY_ID": "demo",
  "AWS_SECRET_ACCESS_KEY": "demo",
  "AWS_STORAGE_BUCKET_NAME": "myapp-static-demo",
  "AWS_S3_REGION_NAME": "us-west-2",
  "AWS_S3_CUSTOM_DOMAIN": "myapp-static-demo.s3.us-west-2.amazonaws.com",
  "AWS_CLOUDFRONT_DOMAIN": "d55ak0y8umkef.cloudfront.net"
}
```

> 🔍 To retrieve secrets from AWS CLI:

```bash
aws secretsmanager describe-secret --secret-id django_app_secrets
aws secretsmanager get-secret-value --secret-id django_app_secrets --version-stage AWSCURRENT
```

---

### 🪣 Amazon S3 Setup

#### ✅ Bucket Name: `myapp-static-demo`

#### 🛡️ Bucket Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowDjangoS3Access",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::590184012044:user/django-app-user"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::myapp-static-demo/*"
    }
  ]
}
```

#### 🌐 CORS Configuration:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "POST", "PUT"],
    "AllowedOrigins": [
      "http://localhost:8000",
      "http://aws-demo.us-west-2.elasticbeanstalk.com/"
    ],
    "ExposeHeaders": [],
    "MaxAgeSeconds": 3000
  }
]
```

---

### 👥 IAM Permissions

#### 🎓 IAM User: `django-app-user`

Policies attached:

* `AdministratorAccess-AWSElasticBeanstalk`
* `AmazonS3FullAccess`
* `SecretsManagerReadWrite`

#### 🧠 EC2 Instance Profile Role: `aws-elasticbeanstalk-ec2-role`

Policies attached:

* `AmazonS3FullAccess`
* `AmazonSSMManagedInstanceCore`
* `AWSElasticBeanstalkMulticontainerDocker`
* `AWSElasticBeanstalkWebTier`
* `AWSElasticBeanstalkWorkerTier`

✅ **Custom ASM Policy (ASM\_policy)**:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:us-west-2:590184012044:secret:django_app_secrets*"
    }
  ]
}
```

---

### 📦 Elastic Beanstalk Configuration

Add this to your `.ebextensions/django.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: "config.settings"
    PYTHONPATH: "/var/app/current:$PYTHONPATH"

  aws:elasticbeanstalk:container:python:
    WSGIPath: config.wsgi:application

container_commands:
  01_makemigrations:
    command: "source /var/app/venv/*/bin/activate && python3 manage.py makemigrations --noinput"
    leader_only: true

  02_migrate:
    command: "source /var/app/venv/*/bin/activate && python3 manage.py migrate --noinput"
    leader_only: true

  03_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python3 manage.py collectstatic --noinput"
    leader_only: true
```

---

### 🐘 CloudWatch Logs with Watchtower

To capture logs from your Django app and send them to CloudWatch:

#### 1. Install Watchtower

```bash
pip install watchtower
```

#### 2. Django `logging` settings

see below
#### 3. To debug errors:

```bash
eb logs | findstr /i "error"
```

---

### 🧪 Useful Commands

```bash
# Activate virtual environment
source /var/app/venv/*/bin/activate

# Navigate to app
cd /var/app/current

# Migrate database
python3 manage.py migrate
```

---

### 🔁 Git Tips for Sync

```bash
# Set remote if repo name changed
git remote set-url origin https://github.com/YOUR_USERNAME/NewRepoName.git

# Fix unrelated history merge
git pull origin main --allow-unrelated-histories

# Push changes
git push -u origin main
```

---

## ✅ Done!

Your Django app should now be:

* Deployed on Elastic Beanstalk
* Serving static files via S3 & CloudFront
* Logging to CloudWatch using Watchtower
* Using AWS Secrets Manager securely
* Fully integrated with GitHub

---








 **AWS CloudWatch logging integration** with your Django app deployed on **Elastic Beanstalk**.

---

## 📘 CloudWatch Logging Setup (AWS + Django)

### Overview

This project integrates AWS CloudWatch logging into the Django app deployed via Elastic Beanstalk using Python’s `logging` framework and the `watchtower` library. Logs are captured for various HTTP events and errors and are streamed to a custom CloudWatch Log Group and Log Stream.

---

### ✅ Prerequisites

* ✅ Django app deployed on **AWS Elastic Beanstalk**
* ✅ EC2 instance with IAM Role: `aws-elasticbeanstalk-ec2-role`
* ✅ IAM User: `django-app-user`
* ✅ Required permissions via IAM policies (see below)

---

### 🛡 IAM Configuration

#### IAM Role: `aws-elasticbeanstalk-ec2-role`

Attached Policies:

* `AdministratorAccess-AWSElasticBeanstalk`
* `AmazonS3FullAccess`
* `AmazonSSMManagedInstanceCore`
* `AWSElasticBeanstalkMulticontainerDocker`
* `AWSElasticBeanstalkWebTier`
* `AWSElasticBeanstalkWorkerTier`
* `CloudWatchLogsFullAccess`
* Custom `cw_policy`
* Custom `ACM_policy`
* `ElasticBeanstalkEnhancedWithUpdates`

> `ACM_policy` includes permission to access Secrets Manager:

```json
{
  "Effect": "Allow",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": "arn:aws:secretsmanager:us-west-2:590184012044:secret:django_app_secrets*"
}
```

> `cw_policy` includes:

```json
{
  "Effect": "Allow",
  "Action": [
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents",
    "logs:DescribeLogGroups",
    "logs:DescribeLogStreams"
  ],
  "Resource": "*"
}
```

#### IAM User: `django-app-user`

Attached Policies:

* Same as above with `AdministratorAccess-AWSElasticBeanstalk`, `AmazonS3FullAccess`, `SecretsManagerReadWrite`, `CloudWatchLogsFullAccess`, `cw_policy`, and `ElasticBeanstalkEnhancedWithUpdates`.

---

### ⚙️ Django `settings.py` Logging Configuration

```python
import boto3
import watchtower

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'watchtower': {
            'level': 'DEBUG',
            'class': 'watchtower.CloudWatchLogHandler',
            'log_group': 'MyLog',
            'stream_name': 'MyStream',
            'create_log_group': True,
            'create_log_stream': True,
            'boto3_client': boto3.client('logs', region_name='us-west-2'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['watchtower', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['watchtower', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

---

### 🧪 Logging Use in `views.py`

Example usage in views:

```python
import logging
logger = logging.getLogger(__name__)

def home(request):
    logger.info("Home page was visited.")
    return render(request, "home.html")

def submit_form(request):
    if request.method == "POST":
        logger.info("Form submitted successfully.")
        name = request.POST.get("name")
        if not name:
            logger.error("Name was not provided in the form.")
            return HttpResponse("Error: Name is required", status=400)
        logger.info(f"Received name: {name}")
        return HttpResponse(f"Hello, {name}!")
    logger.warning("Received an invalid request method.")
    return HttpResponse("Invalid request", status=405)

def crash(request):
    logger.error("🔥 Error triggered from Django route")
    logger.warning("Crash endpoint hit — about to divide by zero!")
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        logger.exception("An exception occurred: ZeroDivisionError")
        return HttpResponse("An error occurred. Please try again later.", status=500)
```

---

### 🔍 How to View Logs

1. Go to the **AWS CloudWatch Console**
2. Navigate to **Log Groups** → `MyLog`
3. Select the **Log Stream** named `MyStream`
4. You’ll see logs for:

   * Home page visits
   * Form submissions (including missing fields)
   * Error triggers (e.g., crashes)

---

### ✅ Verification Tips

* Visit `/` → Should log: `"Home page was visited."`
* Submit form → Should log: `"Form submitted successfully."` and name
* Visit `/crash` → Should log exception and error messages

---
Here's a well-structured `README.md` for the setup process you described:

---

# 📊 Setting Up AWS CloudWatch Metric Filter and Alarm for Django ERROR Logs

This guide walks you through setting up monitoring and alerts for Django error logs in **AWS CloudWatch** using **Watchtower**. You'll create a **Metric Filter** to detect log lines containing the word `"Error"` and configure a **CloudWatch Alarm** to notify you via email when a specified error threshold is exceeded.

---

## 🚀 Prerequisites

* Django application with logging integrated using [Watchtower](https://github.com/kislyuk/watchtower).
* Logs being sent to AWS CloudWatch (e.g., log group: `/aws/CloudWatch/MyLog`).
* Access to AWS Console with CloudWatch and SNS permissions.

---

## 📌 Step 1: Create a Metric Filter for ERROR Logs

1. Log in to the [AWS Console](https://console.aws.amazon.com/).
2. Navigate to **CloudWatch → Logs → Log groups**.
3. Select your Django log group (e.g., `/aws/CloudWatch/MyLog`).
4. Click **Create metric filter**.
5. In the **Filter pattern** field, enter:

   ```
   ?"Error"
   ```
6. *(Optional)* Test the filter pattern to ensure it matches relevant log lines.
7. Click **Next** and configure the metric filter:

   * **Filter name**: `ErrorMetric`
   * **Namespace**: `MyDjangoLogs`
   * **Metric name**: `ErrorCount`
   * **Metric value**: `1`
8. Click **Create filter**.

---

## 🔔 Step 2: Create a CloudWatch Alarm for Error Metrics

1. In **CloudWatch**, go to **Alarms → All alarms**, then click **Create alarm**.
2. Click **Select metric**, then browse:

   ```
   MyDjangoLogs → ErrorCount
   ```
3. Define the alarm condition:

   * **Threshold**: Trigger when `ErrorCount` **≥ 5**
   * **Period**: For **1 datapoint** within **1 minute**
4. Under **Actions**, choose to create or use an existing **SNS topic**:

   * **Topic name**: `ErrorAlerts`
   * **Email recipients**: `your-email@example.com`
5. Create the SNS topic and confirm your subscription via the email AWS sends.
6. Name your alarm, e.g., `ErrorCountAlarm`.
7. Review and **Create alarm**.

---

## ✅ Optional: Test Your SNS Notification

1. Go to **SNS → Topics → ErrorAlerts**.
2. Click **Publish message**.
3. Fill in:

   * **Subject**: `Test Alert`
   * **Message**: `This is a test notification from AWS CloudWatch.`
4. Click **Publish** and confirm you receive the email.

---

## 💡 Notes and Tips

* The pattern `?"Error"` is **case-sensitive** and matches any log line that contains `Error`.
* Adjust the alarm threshold and period based on your app’s criticality and expected error frequency.
* For testing or rapid alerting, use a **1-minute** evaluation period.
* Ensure your Django logs include the word **"Error"** (with correct casing) to be detected by the filter.

---

## 📬 Example Log Snippet from Django

```
ERROR 2024-09-20 15:12:34,567 views 12345 Some error occurred while processing the request
```

---

## 📎 References

* [AWS CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
* [Watchtower GitHub](https://github.com/kislyuk/watchtower)
* [AWS SNS Documentation](https://docs.aws.amazon.com/sns/)

---


