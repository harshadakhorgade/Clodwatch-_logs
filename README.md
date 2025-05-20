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
