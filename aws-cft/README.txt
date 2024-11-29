Cfn Gen

This project generates an AWS CloudFormation (CFT) template using placeholders
for dynamic content. The placeholders are replaced with the appropriate values
during the execution of the script.

Prerequisites:

Before running this project, ensure that you have the following installed on
your machine:

1. Python 3.8 or above
   You can download Python from the official website:
   https://www.python.org/downloads/

   To check if Python is already installed, run the following command in your
   terminal:

   python --version
   or
   python3 --version

2. Pre-commit
   Install Pre-commit, a framework for managing and maintaining multi-language
   pre-commit hooks.

   You can install it using pip:

   pip install pre-commit

How to Run:

1. Create the main CloudFormation template
   - The main CloudFormation template file should be created in the
     `src/template.yaml` file.
   - Use placeholders in the template by following the pattern:

     {{relative file path from src}}

   Example:

     Resources:
       MyBucket:
         Type: "AWS::S3::Bucket"
         Properties:
           BucketName: "{{src/bucket_name.txt}}"

2. Run the script
   - After creating the template with placeholders, run the following command
     to generate the final template:

     python3 cfngen.py

   - This will process the `src/template.yaml` file and replace the placeholders
     with the corresponding values.

3. Resulting Template
   - The generated CloudFormation template will be saved in the
     `template/template.yaml` file.

4. Validate the Generated Template
   - Once the template is generated, you can use AWS CLI or other tools to
     validate the CloudFormation template.

      Once the template is generated, you can use `cfn-lint` to validate the CloudFormation
      template for syntax and best practice issues.

      To install `cfn-lint`, run:

      pip install cfn-lint

      To validate the generated template (`template/template.yaml`), run:

      cfn-lint template/template.yaml

      If the template is valid, `cfn-lint` will exit silently. If there are any issues, it
      will report them along with line numbers and error descriptions.

      Example using `cfn-lint`:

      cfn-lint template/template.yaml

      Alternatively, you can use AWS CLI to validate the template syntax (but note it only
      checks syntax, not best practices):

      aws cloudformation validate-template --template-body file://template/template.yaml


Project Structure:

The basic structure of the project should look like this:

/project-root
  /src
    template.yaml            # Main CloudFormation template with placeholders
    bucket_name.txt          # Text file containing the bucket name (used in
                              # the template)
  /template
    template.yaml            # Final CloudFormation template (generated)
  cfngen.py                  # Python script to generate the final template
  .gitignore                 # Git ignore file to exclude unnecessary files
  pyproject.toml             # Project configuration file for Python dependencies
  .pre-commit-config.yaml    # Pre-commit hook configuration file (if applicable)
  README.txt                 # This file

Notes:

- Ensure that the placeholder pattern {{relative file path from src}} is strictly
  followed for accurate template generation.
- You can add or modify the placeholders according to the needs of your
  CloudFormation template.
- The `bucket_name.txt` file inside the `src` folder is used as a placeholder
  for the bucket name, which is inserted into the template during execution.
- The `.gitignore` file ensures that temporary or generated files (like `.DS_Store`,
  `.pyc`, etc.) are not committed to version control.
- The `pyproject.toml` file is used to manage Python dependencies and project
  metadata.
