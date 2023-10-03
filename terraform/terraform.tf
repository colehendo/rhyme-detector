terraform {
  cloud {
    organization = "colehendo"

    workspaces {
      name = "rhyme-detector"
    }
  }

  required_version = ">= 1.5.0"
}