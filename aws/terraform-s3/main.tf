resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-first-utsavaw"  # Change to a globally unique name

  tags = {
    Name        = "MyTerraformBucket"
    Environment = "Dev"
  }
}
