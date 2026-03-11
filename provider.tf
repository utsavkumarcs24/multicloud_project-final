terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    
  }
}

variable "aws_region" {
  description = "AWS region"
  default     = "ap-south-1"
  type        = string
}

variable "azure_subscription_id" {
  description = "Azure Subscription ID"
  type        = string
  sensitive   = true
}

variable "azure_client_id" {
  description = "Azure Client ID"
  type        = string
  sensitive   = true
}

variable "azure_client_secret" {
  description = "Azure Client Secret"
  type        = string
  sensitive   = true
}

variable "azure_tenant_id" {
  description = "Azure Tenant ID"
  type        = string
  sensitive   = true
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_s3_bucket" "my_storage" {
  bucket = "utsav-gla-bucket-2026"
}

provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
  client_id       = var.azure_client_id
  client_secret   = var.azure_client_secret
  tenant_id       = var.azure_tenant_id
}

resource "azurerm_resource_group" "utsav_rg" {
  name     = "utsav-multi-cloud-rg"
  location = "Central India"
}

resource "azurerm_storage_account" "utsav_azure_storage" {
  name                     = "utsavglaazure2026"
  resource_group_name      = azurerm_resource_group.utsav_rg.name
  location                 = azurerm_resource_group.utsav_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}