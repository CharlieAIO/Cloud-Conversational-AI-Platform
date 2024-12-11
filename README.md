[Repository for frontend](https://github.com/CharlieAIO/Cloud-Conversational-AI-webapp)

## Configuration for AWS and GitHub Actions

*First store the following in GitHub Repository variables:*
  - `AWS_ACCOUNT_ID`
  - `AWS_REGION`

*GitHub Environment Secrets:*
    - `OPENAI_API_KEY` (e.g. sk-proj--Xx-XXXX_xxxx)

1. Create GCP Key
   - Create a new service account
   - Ensure it has permission to use text-to-speech and speech-to-text APIs
   - Create a new key and download it as JSON
   - Store the key in GitHub Actions Secrets under `GCP_KEY_JSON`

2. Create IAM User on AWS
   - Give it `AdministratorAccess-AWSElasticBeanstalk` policy
   - Give it `AmazonEC2ContainerRegistryFullAccess` policy
   - Create Access Key and Secret Key
   - Store them in GitHub Actions Secrets under `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

3. Create Role for Elastic Beanstalk (IAM Instance Profile)
    - Create a new role for EC2
    - Attach `AmazonEC2ContainerRegistryReadOnly` policy to the role
    - Attach `AmazonSSMManagedInstanceCore` policy to the role
    - Attach `AWSElasticBeanstalkWebTier` policy to the role
    - Attach `AWSElasticBeanstalkWorkerTier` policy to the role
    - Attach `AWSElasticBeanstalkMulticontainerDocker` policy to the role

4. Create ECR Repository
    - Create a new repository in ECR
    - Store the repository name in GitHub Repository variables under `ECR_REPOSITORY`

5. Create Elastic Beanstalk Application
    - Create a new Elastic Beanstalk Application
    - Store the application name in GitHub Repository variables under `EB_APPLICATION_NAME`

6. Create Elastic Beanstalk Environment
    - Create a new Elastic Beanstalk Environment
      - Set EC2 Instance Profile to the role created in step 2
      - Set platform to `Docker`
      - Set application code to `Sample application`
      - Set environment type to `Single instance`
      - Set Root volume type to `General Purpose 3`
      - Ensure `IMDSv1` is deactivated
      - Set instance type to `t3.micro`
    - Store the environment name in GitHub Repository variables under `EB_ENVIRONMENT_NAME`

7. Configure Dockerrun.aws.json
    - Edit the json file called `Dockerrun.aws.json`
    - Add the following content to the file:
    - Set the `image` field to the ECR repository URI with the tag `latest`
    - Adjust the port mappings as needed
