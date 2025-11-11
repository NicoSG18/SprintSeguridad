# ***************** Universidad de los Andes ***********************
# ****** Departamento de Ingeniería de Sistemas y Computación ******
# ********** Arquitectura y diseño de Software - ISIS2503 **********
#
# Infraestructura para laboratorio de Autenticación y Autorización
#
# Elementos a desplegar en AWS:
# 1. Grupos de seguridad:
#    - authd-traffic-django (puerto 8080)
#    - authd-traffic-db (puerto 5432)
#    - authd-traffic-ssh (puerto 22)
#
# 2. Instancias EC2:
#    - authd-db (PostgreSQL instalado y configurado)
#    - authd-django (Monitoring app instalada y configurada con Gunicorn)
# ******************************************************************

# Variable. Define la región de AWS donde se desplegará la infraestructura.
variable "region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

# Variable. Define el prefijo usado para nombrar los recursos en AWS.
variable "project_prefix" {
  description = "Prefix used for naming AWS resources"
  type        = string
  default     = "authd"
}

# Variable. Define el tipo de instancia EC2 a usar para las máquinas virtuales.
variable "instance_type" {
  description = "EC2 instance type for application hosts"
  type        = string
  default     = "t2.nano"
}

# Proveedor. Define el proveedor de infraestructura (AWS) y la región.
provider "aws" {
  region = var.region
}

# Variables locales usadas en la configuración de Terraform.
locals {
  project_name = "${var.project_prefix}-authentication"
  repository   = "https://github.com/ISIS2503/ISIS2503-MonitoringApp-Auth0.git"
  # ⚠️ IMPORTANTE: REEMPLAZAR con una clave segura. 
  # Esta clave la lee el settings.py para el manejo de sesiones de Django.
  django_secret_key = "UnaClaveSecretaMuyLargaYUnicaParaProducction-9c+4y&f9rymz$kum_" 

  common_tags = {
    Project   = local.project_name
    ManagedBy = "Terraform"
  }
}

# Data Source. Busca la AMI más reciente de Ubuntu 24.04 usando los filtros especificados.
data "aws_ami" "ubuntu" {
    most_recent = true
    owners      = ["099720109477"]

    filter {
        name   = "name"
        values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
    }

    filter {
        name   = "virtualization-type"
        values = ["hvm"]
    }
}

# Recurso. Define el grupo de seguridad para el tráfico de Django (8080).
resource "aws_security_group" "traffic_django" {
    name        = "${var.project_prefix}-traffic-django"
    description = "Allow application traffic on port 8080"

    ingress {
        description = "HTTP access for service layer"
        from_port   = 8080
        to_port     = 8080
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, {
        Name = "${var.project_prefix}-traffic-django"
    })
}

# Recurso. Define el grupo de seguridad para el tráfico de la base de datos (5432).
resource "aws_security_group" "traffic_db" {
  # ... (inalterado)
  name        = "${var.project_prefix}-traffic-db"
  description = "Allow PostgreSQL access"

  ingress {
    description = "Traffic from anywhere to DB"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # 🎯 MEJORA DE SEGURIDAD: Restringir tráfico de DB solo a la instancia de Django
  # NOTA: Para el laboratorio, lo mantendremos en 0.0.0.0/0, pero idealmente se restringiría.

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-db"
  })
}

# Recurso. Define el grupo de seguridad para el tráfico SSH (22) y permite todo el tráfico saliente.
resource "aws_security_group" "traffic_ssh" {
  # ... (inalterado)
  name        = "${var.project_prefix}-traffic-ssh"
  description = "Allow SSH access"

  ingress {
    description = "SSH access from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-traffic-ssh"
  })
}

# Recurso. Define la instancia EC2 para la base de datos PostgreSQL.
resource "aws_instance" "database" {
  # ... (inalterado)
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_db.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              sudo apt-get update -y
              sudo apt-get install -y postgresql postgresql-contrib

              sudo -u postgres psql -c "CREATE USER monitoring_user WITH PASSWORD 'isis2503';"
              sudo -u postgres createdb -O monitoring_user monitoring_db
              echo "host all all 0.0.0.0/0 trust" | sudo tee -a /etc/postgresql/16/main/pg_hba.conf
              echo "listen_addresses='*'" | sudo tee -a /etc/postgresql/16/main/postgresql.conf
              echo "max_connections=2000" | sudo tee -a /etc/postgresql/16/main/postgresql.conf
              sudo service postgresql restart
              EOT

  tags = merge(local.common_tags, {
    Name = "${var.project_prefix}-db"
    Role = "database"
  })
}

# Recurso. Define la instancia EC2 para la aplicación de Monitoring (Django).
# 🎯 CORREGIDO: Se configura el entorno, Gunicorn, y Systemd para que la app se ejecute.
resource "aws_instance" "monitoring" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.traffic_django.id, aws_security_group.traffic_ssh.id]

  user_data = <<-EOT
              #!/bin/bash

              # --- 1. CONFIGURACIÓN DEL ENTORNO DE PRODUCCIÓN ---
              DB_HOST="${aws_instance.database.private_ip}"
              PUBLIC_IP="${aws_instance.monitoring.public_ip}"

              # Crear archivo de entorno /etc/django_env
              echo "DATABASE_HOST=$DB_HOST" | sudo tee /etc/django_env
              echo "DATABASE_NAME=monitoring_db" | sudo tee -a /etc/django_env
              echo "DATABASE_USER=monitoring_user" | sudo tee -a /etc/django_env
              echo "DATABASE_PASSWORD=isis2503" | sudo tee -a /etc/django_env
              
              # Variables de Django (Leídas por settings.py)
              echo "SECRET_KEY=${local.django_secret_key}" | sudo tee -a /etc/django_env 
              echo "DEBUG=False" | sudo tee -a /etc/django_env
              echo "ALLOWED_HOSTS=$PUBLIC_IP" | sudo tee -a /etc/django_env
              
              # Variable usada para el Logout Redirect de Auth0
              echo "EXTERNAL_URL=http://$PUBLIC_IP:8080" | sudo tee -a /etc/django_env 

              # --- 2. INSTALACIÓN DE DEPENDENCIAS ---
              # Instala Python, Git, dependencias de DB, Entorno Virtual y Gunicorn
              sudo apt-get update -y
              sudo apt-get install -y python3-pip git build-essential libpq-dev python3-dev python3-venv gunicorn

              # --- 3. CLONACIÓN Y CONFIGURACIÓN DEL PROYECTO ---
              mkdir -p /labs
              cd /labs
              git clone ${local.repository}
              cd ISIS2503-MonitoringApp-Auth0
              
              # Usar entorno