terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
      }
    }
}

provider "aws" {
    region = "us-east-2"
}

resource "aws_iam_role" "lambda_role" {
    name   = "get_riot_api_match_data_into_s3_Lambda_Function_Role"
    assume_role_policy = <<EOF
{
"Version": "2012-10-17",
"Statement": [
{
"Action": "sts:AssumeRole",
"Principal": {
"Service": "lambda.amazonaws.com"
},
"Effect": "Allow",
"Sid": ""
}
]
}
EOF
}

resource "aws_iam_policy" "iam_policy_for_lambda" {
 
    name         = "aws_iam_policy_for_terraform_aws_lambda_role"
    path         = "/"
    description  = "AWS IAM Policy for managing aws lambda role"
    policy = <<EOF
{
"Statement": [
{
"Action": [
"logs:CreateLogGroup",
"logs:CreateLogStream",
"logs:PutLogEvents"
],
"Effect": "Allow",
"Resource": "arn:aws:logs:*:*:*"
},
{
"Sid": "LambdaS3ReadAccess",
"Effect": "Allow",
"Action": [
"s3:PutObject"
],
"Resource": [
"arn:aws:s3:::league-of-legends-data-engineering-project/raw_league_entry_dto/*"
]
},
{
"Sid": "LambdaSecretManagerReadSecretAccess",
"Effect": "Allow",
"Action": [
"secretsmanager:GetSecretValue"
],
"Resource": [
"arn:aws:secretsmanager:us-east-2:506488007941:secret:riot-games-api-Y0VYUf"
]
}
],
"Version": "2012-10-17"
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
    role        = aws_iam_role.lambda_role.name
    policy_arn  = aws_iam_policy.iam_policy_for_lambda.arn
}

resource "null_resource" "pip_install" {
    triggers = {
        shell_hash = "${sha256(file("${path.module}/requirements.txt"))}"
    }

    provisioner "local-exec" {
        command = "py -m pip install -r ${path.module}/requirements.txt -t ${path.module}/layer/python"
    }
}

data "archive_file" "zip_get_league_entries" {
    type        = "zip"
    source_dir  = "${path.module}/code"
    output_path = "${path.module}/get_league_entries.zip"
    excludes = ["logs", "venv", "__pycache__", "requirements.txt"]
}

data "archive_file" "layer" {
    type        = "zip"
    source_dir  = "${path.module}/layer"
    output_path = "${path.module}/layer.zip"
    depends_on  = [null_resource.pip_install]
}

resource "aws_lambda_layer_version" "layer" {
    layer_name          = "test-layer"
    filename            = data.archive_file.layer.output_path
    source_code_hash    = data.archive_file.layer.output_base64sha256
    compatible_runtimes = ["python3.12", "python3.9", "python3.8", "python3.7", "python3.6"]
}


resource "aws_lambda_function" "get_riot_api_match_data_into_s3" {
    filename                       = "${path.module}/get_league_entries.zip"
    function_name                  = "get_riot_api_match_data_into_s3"
    role                           = aws_iam_role.lambda_role.arn
    handler                        = "main.lambda_handler"
    runtime                        = "python3.12"
    timeout                        = 10
    depends_on                     = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
    layers                         = [aws_lambda_layer_version.layer.arn]

    environment {
        variables = {
            BUCKET = "league-of-legends-data-engineering-project"
        }
    }
}

output "get_riot_api_match_data_into_s3_arn" {
    value = aws_lambda_function.get_riot_api_match_data_into_s3.arn
    description = "The ARN of the Lambda function get_riot_api_match_data_into_s3"
}

output "get_riot_api_match_data_into_s3_function_name" {
    value = aws_lambda_function.get_riot_api_match_data_into_s3.function_name
    description = "The function name of the Lambda function get_riot_api_match_data_into_s3"
}
