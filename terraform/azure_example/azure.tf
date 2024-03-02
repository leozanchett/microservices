terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.94.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg_example" {
  name     = "aula"
  location = "East US"
}

resource "azurerm_virtual_network" "example" {
  name                = "sample-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg_example.location
  resource_group_name = azurerm_resource_group.rg_example.name
}

resource "azurerm_subnet" "example" {
  name                 = "sample-subnet"
  resource_group_name  = azurerm_resource_group.rg_example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_network_interface" "example" {
  name                = "sample-nic"
  location            = azurerm_resource_group.rg_example.location
  resource_group_name = azurerm_resource_group.rg_example.name

  ip_configuration {
    name                          = "testconfiguration1"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "example" {
  name                  = "SampleVM"
  location              = azurerm_resource_group.rg_example.location
  resource_group_name   = azurerm_resource_group.rg_example.name
  network_interface_ids = [azurerm_network_interface.example.id]
  size                  = "Standard_B2s"

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  os_disk {
    name                 = "myosdisk-example"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  admin_username                  = "testadmin"
  admin_password                  = "Password1234!"
  disable_password_authentication = false
}

output "public_ip" {
  value = azurerm_linux_virtual_machine.example.public_ip_address
}