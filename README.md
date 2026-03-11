# Multicloud Deployment API

A Flask-based REST API for deploying infrastructure across AWS and Azure using Terraform.

## 📋 Prerequisites

- Python 3.8+
- Terraform 1.0+
- AWS Account (for S3 deployments)
- Azure Account (for Storage Account deployments)

## 🚀 Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Azure Credentials

Create `terraform.tfvars` from the example file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` and add your Azure credentials:

```hcl
azure_subscription_id = "your-actual-subscription-id"
azure_client_id       = "your-actual-client-id"
azure_client_secret   = "your-actual-client-secret"
azure_tenant_id       = "your-actual-tenant-id"
aws_region            = "ap-south-1"
```

### 3. Initialize Terraform

```bash
terraform init
```

## 📌 API Endpoints

### Deploy Cloud Resources

**POST** `/deploy`

Deploy AWS S3 bucket or Azure Storage Account.

**Request:**
```json
{
  "cloud": "aws"
}
```

**Response:**
```json
{
  "status": "Success",
  "message": "AWS Bucket created!"
}
```

**Supported Cloud Providers:**
- `aws` - Deploy AWS S3 bucket
- `azure` - Deploy Azure Storage Account

### Check API Status

**GET** `/status`

Verify API is running.

**Response:**
```json
{
  "status": "API is running"
}
```

## 🏃 Running the Application

```bash
python main.py
```

The API server will start on `http://localhost:8080`

## 📁 Project Structure

```
.
├── main.py                    # Flask API application
├── aws_connector.py           # AWS S3 utility module
├── provider.tf                # Terraform configuration (AWS + Azure)
├── requirements.txt           # Python dependencies
├── terraform.tfvars.example   # Example credentials template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🔐 Security Notes

⚠️ **Never commit `terraform.tfvars` to version control!**

The `.gitignore` file already protects:
- `.tfstate` files
- `terraform.tfvars`
- Python cache files (`__pycache__`, `.pyc`)

## 🐛 Error Handling

The API handles various error scenarios:

| Error | HTTP Code | Solution |
|-------|-----------|----------|
| No JSON data provided | 400 | Ensure request body contains valid JSON |
| Unsupported cloud provider | 400 | Use 'aws' or 'azure' only |
| Terraform execution failed | 500 | Check Terraform logs and AWS/Azure credentials |
| Unexpected error | 500 | Check application logs |

## 📊 Testing with curl

### Test Status Endpoint
```bash
curl http://localhost:8080/status
```

### Deploy AWS Resources
```bash
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{"cloud": "aws"}'
```

### Deploy Azure Resources
```bash
curl -X POST http://localhost:8080/deploy \
  -H "Content-Type: application/json" \
  -d '{"cloud": "azure"}'
```

## 💡 Using AWS Connector Module

```python
from aws_connector import AWSConnector

# Initialize connector
aws = AWSConnector(region='ap-south-1')

# List buckets
buckets = aws.list_buckets()

# Upload file
aws.upload_file('my-bucket', 'local-file.txt', 'remote-file.txt')

# Check bucket exists
exists = aws.bucket_exists('my-bucket')

# List objects
objects = aws.list_objects('my-bucket')
```

## 🔧 Troubleshooting

**Issue:** `terraform: command not found`
- **Solution:** Install Terraform from https://www.terraform.io/downloads

**Issue:** AWS credentials not found
- **Solution:** Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables

**Issue:** Azure authentication failed
- **Solution:** Verify `terraform.tfvars` has correct Azure credentials and the service principal has necessary permissions

## 📝 Logs

Application logs are output to the console with level `INFO`. Check logs for detailed error information during deployment.

## 📄 License

This project is provided as-is for educational purposes.
