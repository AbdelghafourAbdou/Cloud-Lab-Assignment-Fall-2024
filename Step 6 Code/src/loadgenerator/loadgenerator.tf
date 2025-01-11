provider "google" {
    credentials = file("externalLoadGenerator.json")
    project     = "cloudlabapoli"
    region      = "us-central1"
    zone        = "us-central1-a"
}

resource "tls_private_key" "ssh_key" {
    algorithm = "RSA"
    rsa_bits  = 2048
}

resource "google_compute_instance" "load_generator_vm" {
    name         = "load-generator-${count.index}"
    machine_type = "e2-standard-2"
    count        = 3

    boot_disk {
        initialize_params {
        image = "debian-cloud/debian-11"
        }
    }

    network_interface {
        network = "default"
        access_config {}
    }

    metadata = {
        ssh-keys = "debian:${tls_private_key.ssh_key.public_key_openssh}"
    }
}

resource "null_resource" "provision_vm" {
    depends_on = [google_compute_instance.load_generator_vm]
    count = 3

    provisioner "file" {
        source      = "loadgenerator.sh"
        destination = "/tmp/loadgenerator.sh"

        connection {
        type        = "ssh"
        user        = "debian"
        private_key = tls_private_key.ssh_key.private_key_pem
        host        = google_compute_instance.load_generator_vm[count.index].network_interface.0.access_config.0.nat_ip
        }
    }

    provisioner "file" {
        source      = "env.list"
        destination = "/tmp/env.list"

        connection {
        type        = "ssh"
        user        = "debian"
        private_key = tls_private_key.ssh_key.private_key_pem
        host        = google_compute_instance.load_generator_vm[count.index].network_interface.0.access_config.0.nat_ip
        }
    }

    provisioner "remote-exec" {
        inline = [
        "chmod +x /tmp/loadgenerator.sh",
        "cd /tmp",
        "./loadgenerator.sh"
        ]

        connection {
        type        = "ssh"
        user        = "debian"
        private_key = tls_private_key.ssh_key.private_key_pem
        host        = google_compute_instance.load_generator_vm[count.index].network_interface.0.access_config.0.nat_ip
        }
    }
}

output "vm_ip" {
    value = google_compute_instance.load_generator_vm[*].network_interface.0.access_config.0.nat_ip
}
