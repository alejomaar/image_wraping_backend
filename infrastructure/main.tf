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
  name   = "${var.app_name}_${data.archive_file.app_zip.output_md5}.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.app_zip.output_path
}

resource "google_cloudfunctions_function" "function" {
  name        = "terrafom-function"
  description = "description"
  runtime     = "python312"

  available_memory_mb   = 128
  timeout               = 60
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  entry_point           = "main"
  labels = {
    my-label = "my-label-value"
  }
  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = "projects/nth-micron-411415/topics/terraform-test"
  }
}

