resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-terraform-bucket-12345"

  tags = {
    Name        = "MyTerraformBucket"
    Environment = "Dev"
  }
}