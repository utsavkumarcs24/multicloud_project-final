from flask import Flask, request, jsonify
import subprocess
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TERRAFORM_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/deploy', methods=['POST'])
def deploy():
    try:
        logging.info('Request data: %s', request.data)
        
        data = request.get_json(force=True, silent=True)
        logging.info('Parsed JSON: %s', data)
        
        if not data:
            return jsonify({"status": "Error", "message": "No JSON data provided. Send JSON body with 'cloud' key."}), 400
        
        cloud = data.get('cloud', 'aws').lower()
        
        # Terraform init
        init_result = subprocess.run(
            "terraform init",
            capture_output=True, text=True,
            cwd=TERRAFORM_DIR,
            shell=True
        )
        if init_result.returncode != 0:
            logging.error("Terraform init failed: %s", init_result.stderr)
            return jsonify({"status": "Error", "message": f"Terraform init failed: {init_result.stderr}"}), 500
        
        if cloud == 'aws':
            result = subprocess.run(
                "terraform apply -target=aws_s3_bucket.my_storage -var-file=terraform.tfvars -auto-approve",
                capture_output=True, text=True,
                cwd=TERRAFORM_DIR,
                shell=True
            )
            if result.returncode == 0:
                return jsonify({"status": "Success", "message": "AWS Bucket created!"}), 200
            else:
                logging.error("Terraform apply failed: %s", result.stderr)
                return jsonify({"status": "Error", "message": f"Deployment failed: {result.stderr}"}), 500
        
        elif cloud == 'azure':
            result = subprocess.run(
                "terraform apply -target=azurerm_storage_account.utsav_azure_storage -target=azurerm_resource_group.utsav_rg -var-file=terraform.tfvars -auto-approve",
                capture_output=True, text=True,
                cwd=TERRAFORM_DIR,
                shell=True
            )
            if result.returncode == 0:
                return jsonify({"status": "Success", "message": "Azure Storage Account created!"}), 200
            else:
                logging.error("Terraform apply failed: %s", result.stderr)
                return jsonify({"status": "Error", "message": f"Deployment failed: {result.stderr}"}), 500
        
        else:
            return jsonify({"status": "Error", "message": f"Unsupported cloud provider: {cloud}. Use 'aws' or 'azure'."}), 400
            
    except Exception as e:
        logging.error("Unexpected error: %s", e, exc_info=True)
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)