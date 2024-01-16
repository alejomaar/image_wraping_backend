data "archive_file" "app_zip" {
  type        = "zip"
  source_dir  = "../app"
  output_path = "../build/app.zip"
}

resource "google_storage_bucket" "bucket" {
  name     = "${var.app_name}-test-bucket"
  location = "US"
}


resource "google_storage_bucket_object" "archive" {
  name   = "index.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.app_zip.output_path
}

resource "google_cloudfunctions_function" "function" {
  name        = "terrafom-function"
  description = "My function"
  runtime     = "python312"

  available_memory_mb   = 128
  timeout               = 60
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  entry_point           = "main"
}

