
data "template_file" "environment_variables_json" {
  template = file("${path.module}/environment/${local.ENVIRONMENT_VAR_FILE[var.environment]}")
  vars = {
    frontend_url = "https://${local.FE_WEB_DOMAIN[var.environment]}"
    backend_url = "https://${local.API_DOMAIN[var.environment]}"
    load_fixtures = var.load_fixtures
    fixture_list = var.fixture_list
    git_branch = var.git_branch
    git_hash = var.git_hash
  }
}
