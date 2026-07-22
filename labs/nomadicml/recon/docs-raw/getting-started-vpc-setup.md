> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Self-Hosted VPC Setup

> Deploy Nomadic in your own AWS or GCP virtual private cloud.

# Self-Hosted Nomadic VPC Setup

Nomadic supports private deployments in customer-controlled AWS and GCP environments. We bring the application, deployment automation, and model-serving configuration; you keep control of the cloud account, network boundaries, IAM policies, logs, storage, and data residency.

The standard setup is intentionally simple: point Nomadic at an existing private network, provide a small set of infrastructure inputs, and we deploy the web app, API, storage, database, and model endpoints with Terraform-backed infrastructure.

<Note>
  VPC deployments can be accessed through your VPN, Direct Connect, Cloud VPN, Cloud Interconnect, private DNS, or any other access pattern your security team already uses. Public ingress is not required.
</Note>

## Deployment Models

<CardGroup cols={2}>
  <Card title="AWS VPC" icon="server">
    Deploy into a new or existing AWS VPC with an internal ALB, private EC2 app instances, S3 locked to a VPC endpoint, optional DocumentDB, ECR, SSM operations, and SageMaker model endpoints.
  </Card>

  <Card title="GCP VPC" icon="cloud">
    Deploy into a GCP project/VPC with Compute Engine backends, HTTPS load balancing, Artifact Registry, Secret Manager, Memorystore Redis, firewall rules, Cloud NAT, and IAP-based admin access.
  </Card>
</CardGroup>

## What We Need From You

For either cloud, Nomadic only needs the information required to land in your existing network and match your security model.

### AWS Inputs

* AWS account ID, target region, and the IAM role/profile Nomadic should use for deployment.
* Existing VPC ID, VPC CIDR, private subnet IDs, and an S3 Gateway VPC endpoint ID. If the endpoint is missing, we can provision the baseline endpoint prerequisites first.
* Allowed ingress CIDRs for the internal load balancer, usually your VPC CIDR, VPN CIDRs, or corporate network ranges.
* Domain name and optional ACM certificate ARN if you want HTTPS terminated at the internal ALB.
* Whether metadata should run on Amazon DocumentDB or the managed Mongo-compatible database provisioned with the deployment.
* Model-serving preference: AWS SageMaker endpoints, an existing private inference endpoint, or a hybrid configuration.

### GCP Inputs

* GCP project, region, zones, and the service account Nomadic should use for deployment.
* CIDR range for the dedicated Nomadic subnet.
* Domain names and DNS ownership for managed HTTPS certificates.
* Machine sizes for staging and production API workers.
* Secret Manager access policy, Artifact Registry location, and any required firewall allowlists.
* Optional Redis/Memorystore and private service networking requirements.

## AWS: How It Works

Our AWS VPC deployment is backed by Terraform modules that can either create a private-only VPC or attach to an existing customer VPC. The app stack creates an internal Application Load Balancer, routes `/` to the web service and `/api/*` to the backend API, and places the backing instances in private subnets.

Customer data stays inside the customer account. Video objects are stored in an S3 bucket whose policy can be locked to the S3 Gateway VPC endpoint, so reads and writes stay on the private AWS path. The backend uses IAM roles rather than long-lived access keys wherever possible, including role-based S3 imports from customer buckets.

Inference can run next to the app stack through model-specific SageMaker endpoints. We support separating the application layer from model compute so that each model can be deployed, resized, or replaced independently. This is the pattern we use for large VLM endpoints, OCR, segmentation, and related GPU workloads.

### AWS Bringup Flow

1. Confirm whether we are creating a fresh VPC or attaching to an existing VPC.
2. Apply the VPC prerequisite stack if the existing network is missing required endpoints.
3. Apply the Nomadic app stack: internal ALB, private web/API instances, IAM, ECR, S3, logging, and optional DocumentDB.
4. Build and push the model images, then apply the model-specific compute stacks.
5. Deploy the backend container through SSM and verify `/health`, `/api/health`, and model routing from inside the VPC.

In practice, most customer-specific setup is captured in a small Terraform variable file: VPC IDs, subnet IDs, CIDR allowlists, region, instance sizes, tags, and model endpoint names.

## GCP: How It Works

Nomadic also supports GCP VPC deployments with a cloud-native infrastructure pattern. Terraform provisions a dedicated VPC/subnet, places backend VMs in Compute Engine, fronts them with managed HTTPS load balancing, and stores deployable images in Artifact Registry.

The GCP stack includes the pieces needed for a production service: firewall rules for load balancer health checks, optional IAP SSH for operator access, Cloud NAT for controlled outbound access, Secret Manager for runtime secrets, Cloud Logging/Monitoring, Memorystore Redis, and private service networking where needed.

During deployment, we push the backend image to Artifact Registry, start the container with the approved runtime environment, wait for local health, and then wait for the GCP backend service to report healthy.

### GCP Bringup Flow

1. Confirm project, region, DNS names, service accounts, and network boundaries.
2. Apply the Terraform baseline for VPC, subnet, firewall, load balancers, Artifact Registry, Secret Manager, Redis, and IAM.
3. Populate approved secrets in Secret Manager.
4. Run the deploy workflow to install and start the backend container on each VM.
5. Verify managed certificate status, load balancer health, and API health checks.

As with AWS, the deployment is mostly a small variable file: project ID, region, zones, domains, subnet CIDR, machine sizes, Artifact Registry location, and IAM labels. The result is a private, cloud-native GCP deployment that your infrastructure team can inspect and operate using standard GCP controls.

## Security And Operations

* Network ingress is controlled by your VPC, firewall rules, security groups, load balancer configuration, and private connectivity.
* Storage access uses cloud-native identity: AWS instance roles for S3 and GCP service accounts for GCS/Artifact Registry/Secret Manager.
* Model compute is configurable per deployment. AWS customers can use SageMaker-backed endpoints; GCP customers can use approved private inference endpoints or a customer-specific model-serving plan.
* Updates are repeatable because infrastructure is Terraform-managed and application rollout is automated.

## Support

To start a VPC deployment, contact your Nomadic representative or email [support@nomadicml.com](mailto:support@nomadicml.com). We will review your target cloud, network requirements, security constraints, and model-serving needs, then provide the exact Terraform inputs for your environment.
