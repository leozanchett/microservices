# Este código é compatível com a versão 4.25.0 do Terraform e com as que têm compatibilidade com versões anteriores à 4.25.0.
# Para informações sobre como validar esse código do Terraform, consulte https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#format-and-validate-the-configuration

resource "google_compute_instance" "instance-20240302-193807" {
  boot_disk {
    auto_delete = true
    device_name = "instance-20240302-193807"

    initialize_params {
      image = "projects/cos-cloud/global/images/cos-stable-109-17800-147-22"
      size  = 10
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    container-vm = "cos-stable-109-17800-147-22"
    goog-ec-src  = "vm_add-tf"
  }

  machine_type = "e2-small"

  metadata = {
    gce-container-declaration = "spec:\n  containers:\n  - name: instance-20240302-193807\n    image: dwizard/ia_pdf_classifier\n    stdin: false\n    tty: false\n  restartPolicy: Always\n# This container declaration format is not public API and may change without notice. Please\n# use gcloud command-line tool or Google Cloud Console to run Containers on Google Compute Engine."
  }

  name = "instance-20240302-193807"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/datafinance-d39db/regions/us-central1/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "949442627237-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/devstorage.read_only", "https://www.googleapis.com/auth/logging.write", "https://www.googleapis.com/auth/monitoring.write", "https://www.googleapis.com/auth/service.management.readonly", "https://www.googleapis.com/auth/servicecontrol", "https://www.googleapis.com/auth/trace.append"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  tags = ["http-server", "https-server"]
  zone = "us-central1-c"
}
