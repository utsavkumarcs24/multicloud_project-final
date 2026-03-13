resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-first-UTSAVKUMAR234"  # Change to a globally unique name

  tags = {
    Name        = "MyTerraformBucket"
    Environment = "Dev"
  }
}
