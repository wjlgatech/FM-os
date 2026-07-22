> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Cloud Storage Uploads

> Securely upload videos from AWS, GCP, or Azure using direct cloud integration or signed URLs.

# Uploading From Cloud Storage

Use the Nomadic web portal to connect cloud buckets and import videos without leaving the browser. In the app, open **Profile → Cloud Integrations** to launch the guided workflow, upload credentials, optionally save the connection, and pick files to ingest. The sections below outline the IAM setup each modal expects before you start the import.

### Google Cloud Storage (Web UI)

The UI walks through the same steps outlined below. Use these instructions to generate the service account credentials the modal requests:

1. **Create a service account**
   * In the Google Cloud Console, go to **IAM & Admin → Service accounts → Create**.
   * Name the account (for example `nomadic-importer`) and finish the creation wizard.
2. **Grant the account read access to your bucket**
   * Open **Cloud Storage → Browser**, select the bucket that holds your videos, and open the **Permissions** tab.
   * Click **Grant access**, add the service-account email, and assign both **Storage Object Viewer** and **Storage Legacy Bucket Reader** roles so that hierarchical listings work.
3. **Create and download a JSON key**
   * Return to the service account, choose **Manage keys → Add key → Create new key → JSON → Create**.
   * Download the `.json` file and keep it secure—Google will not show it again.
4. **Upload the credentials in Nomadic**
   * In **Profile → Cloud Integrations**, click **Add Google Cloud Storage** and upload the JSON key in Step 1 of the modal.
   * Provide the bucket name and optional prefix in Step 2, then test the connection. You can choose to save the integration for future imports.
5. **Select files and import**
   * After the connection succeeds, pick the videos you want to ingest. Nomadic will use the uploaded key once to read the selected files.

Saved integrations appear at the top of the Cloud Integrations tab so you can reuse them without re-uploading keys.

### Amazon S3 / S3-Compatible Storage (Web UI)

Follow these steps to supply the credentials that the S3 modal expects:

1. **Create a least-privilege IAM policy**
   * In the AWS Console, open **IAM → Policies → Create policy → JSON**.
   * Paste a policy that grants `s3:ListBucket` on your bucket and `s3:GetObject` on the objects you plan to ingest. Example:

     ```json theme={null}
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": "s3:ListBucket",
           "Resource": "arn:aws:s3:::your-bucket-name",
           "Condition": { "StringLike": { "s3:prefix": ["optional/prefix/*", "optional/prefix"] } }
         },
         {
           "Effect": "Allow",
           "Action": ["s3:GetObject"],
           "Resource": "arn:aws:s3:::your-bucket-name/optional/prefix/*"
         }
       ]
     }
     ```
   * Adjust the bucket ARN (and prefix if you only want to expose a folder). You can use AWS's visual editor if you prefer.
2. **Create an IAM user for Nomadic AI**
   * Still in IAM, go to **Users → Create user** and enable **Access key - Programmatic access**.
   * Attach the policy from Step 1 (or `AmazonS3ReadOnlyAccess` if you want full read-only coverage of the bucket).
3. **Store the access keys**
   * After the user is created, download the `.csv` or copy the `Access key ID` and `Secret access key`. AWS will not show the secret again.
4. **Enter the credentials in Nomadic**
   * In **Profile → Cloud Integrations**, choose **Add S3-Compatible Bucket**. Step 1 asks for the access key, secret key, optional session token, the region, and an optional custom endpoint URL.
   * Step 2 prompts for the bucket name and an optional prefix. Enable "Save this integration" if you want to reuse it.
5. **Validate, pick files, and import**
   * The modal tests the credentials and lists your objects. Select the videos you want, then continue to kick off the import flow.

Saved S3 integrations also appear in the Cloud Integrations tab, so future imports only require choosing the integration and prefix.

For Cloudflare R2 and other S3-compatible providers:

* Keep using `s3://bucket/key.mp4` URIs in SDK/API upload calls.
* Save the provider's custom endpoint in the S3 integration (for R2 this is typically `https://<account>.r2.cloudflarestorage.com`).
* Use the provider's recommended region value. For Cloudflare R2 this is usually `auto`.

### Amazon S3 for MCAP Cloud Ingest

MCAP cloud ingest uses AWS IAM role federation and Google Storage Transfer
Service. This is separate from the access-key S3 integration used for normal
video imports: the backend starts a cloud-to-cloud transfer from your S3 bucket
into Nomadic storage, then processes the MCAP after the copied object is present.

1. **Fetch the Google identity to trust**

   ```python theme={null}
   setup = client.cloud_integrations.get_s3_storage_transfer_setup()

   print(setup["google_service_account_subject_id"])
   print(setup["aws_trust_policy_template"])
   ```

2. **Create an IAM policy with read-only access to the MCAP prefix**

   Replace `your-mcap-bucket` and `mcap/` with your bucket and prefix.

   ```json theme={null}
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "s3:ListBucket",
         "Resource": "arn:aws:s3:::your-mcap-bucket",
         "Condition": {
           "StringLike": {
             "s3:prefix": ["mcap/", "mcap/*"]
           }
         }
       },
       {
         "Effect": "Allow",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::your-mcap-bucket/mcap/*"
       }
     ]
   }
   ```

   The role does not need delete access.

3. **Create an IAM role trusted by Google Storage Transfer**

   In AWS IAM, create a role with a custom trust policy. Use the exact
   `google_service_account_subject_id` returned by
   `get_s3_storage_transfer_setup()`.

   ```json theme={null}
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "accounts.google.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "accounts.google.com:sub": "<google_service_account_subject_id>"
           }
         }
       }
     ]
   }
   ```

   Attach the read-only S3 policy from Step 2 to this role, then copy the role ARN.

4. **Save the Storage Transfer integration**

   ```python theme={null}
   integration = client.cloud_integrations.add_s3_storage_transfer(
       name="MCAP archive",
       bucket="your-mcap-bucket",
       prefix="mcap/",
       role_arn="arn:aws:iam::123456789012:role/NomadicMcapTransferRole",
   )
   ```

5. **Start an MCAP cloud ingest**

   ```python theme={null}
   job = client.upload(
       "s3://your-mcap-bucket/mcap/example-017-droid-ds.mcap",
       folder="mcap_cloud_test",
       integration_id=integration["id"],
       wait_for_uploaded=False,
   )

   final = client.wait_for_mcap_import_job(
       job["mcap_import_job_id"],
       timeout=7200,
   )
   ```

<Note>
  Use the role-based `s3_storage_transfer` integration for `.mcap` imports. The
  access-key S3 integration above remains the correct setup for normal `.mp4`
  cloud video imports.
</Note>

### Hugging Face Buckets (Web UI)

Nomadic can also pull videos from Hugging Face Storage Buckets using a stored Hugging Face token.

1. **Create a Hugging Face token**
   * In Hugging Face, open **Settings → Access Tokens**.
   * Prefer a **fine-grained** token if Hugging Face exposes the bucket access you need.
   * If bucket scoping is not available, use a dedicated Hugging Face account or storage-only token for Nomadic imports.
2. **Open the Hugging Face modal in Nomadic**
   * Go to **Profile → Cloud Integrations → Add Hugging Face Bucket**.
   * Enter the token, bucket id in `namespace/name` format, and an optional prefix.
3. **Validate and preview files**
   * Nomadic tests the token against the bucket and lists readable video files.
   * You can save the integration so later imports do not require re-entering the token.
4. **Import into a Nomadic folder**
   * Select the files you want and continue to the normal upload/import modal.
   * Imported videos are stored as standard Nomadic videos and can be analyzed like any other upload.

With either integration in place, the Profile page lets you reopen the modal at any time to browse your bucket and launch new imports straight from the web portal—no additional setup required.
