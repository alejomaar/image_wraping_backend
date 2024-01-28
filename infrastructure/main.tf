data "archive_file" "app_zip" {
  type        = "zip"
  source_dir  = "../app"
  output_path = "../build/app.zip"
  excludes    = concat(
    tolist(fileset("../app", "notebook/*")),
    tolist(fileset("../app", "img/*"))
  )
}

resource "google_storage_bucket" "bucket" {
  name     = "${var.app_name}-app-bucket"
  location = "US"
}


resource "google_storage_bucket_object" "archive" {
  name   = "${var.app_name}_${data.archive_file.app_zip.output_md5}.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.app_zip.output_path
}

resource "google_cloudfunctions2_function" "default" {
  name        = "function"
  location    = var.gcp_region
  description = "a new function"

  build_config {
    runtime     = "python312"
    entry_point = "main" # Set the entry point
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.archive.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
  }
}

output "function_uri" { 
  value = google_cloudfunctions2_function.default.service_config[0].uri
}

output "bucketname" { 
  value = google_storage_bucket.bucket.name
}

output "archivename" { 
  value = google_storage_bucket_object.archive.name
}


