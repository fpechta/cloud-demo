variable "resource_group_name" {
  description = "Name der Resource Group"
  default     = "rg-health-checker"
}

variable "location" {
  description = "Azure Region"
  default     = "westeurope"
}

variable "storage_account_name" {
  description = "Name des Storage Accounts (global unique)"
  default     = "sthealthcheckerfp2905"
}

variable "aks_cluster_name" {
  description = "Name des AKS Clusters"
  default     = "aks-health-checker"
}

variable "aks_dns_prefix" {
  description = "DNS Prefix für AKS"
  default     = "healthchecker"
}

variable "acr_name" {
  description = "Name der Azure Container Registry (global unique)"
  default     = "acrhealthcheckerfp2905"
}