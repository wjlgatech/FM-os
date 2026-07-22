> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# API Authentication

> How to authenticate with the Nomadic API

# Authentication

To use the Nomadic API, you need to authenticate your requests using an API key. This guide covers obtaining and using API keys with both the SDK and direct HTTP requests.

## Obtaining an API Key

Generate API keys from the Nomadic web platform:

1. Log in to your account at [app.nomadicml.com](https://app.nomadicml.com)
2. Navigate to your profile by clicking your avatar in the top-right corner
3. Select **API Keys** from the menu
4. Click **Generate New Key**
5. Enter a descriptive name for your key
6. Select the expiration period (default is 90 days)
7. Click **Create Key**

<Warning>
  The full API key is only shown once when generated. Copy and store it securely. Lost keys cannot be recovered and must be regenerated.
</Warning>

## Using the Python SDK

Initialize the Nomadic client with your API key:

```python theme={null}
from nomadic import NomadicAI

# Basic initialization
client = NomadicAI(api_key="your_api_key")

# With custom configuration
client = NomadicAI(
    api_key="your_api_key",
    base_url="https://api.nomadic.company_name.com/",  # Custom endpoint for VPC setups
    timeout=900  # Request timeout in seconds
)

# Verify authentication
auth_info = client.verify_auth()
print("Authentication successful:", auth_info)
```

### Configuration Parameters

| Parameter  | Type  | Default                             | Description                     |
| ---------- | ----- | ----------------------------------- | ------------------------------- |
| `api_key`  | `str` | None                                | Your Nomadic API key (required) |
| `base_url` | `str` | `"https://api-prod.nomadicml.com/"` | API endpoint URL                |
| `timeout`  | `int` | `900`                               | Request timeout in seconds      |

## Verifying Authentication

Test your API key validity:

**SDK Method:**

```python theme={null}
auth_info = client.verify_auth()
```

## Troubleshooting

**Invalid API Key** - If you receive an `AuthenticationError`:

* Verify you're using the correct API key
* Check if the key has expired or been revoked

```python theme={null}
try:
    client = NomadicAI(api_key="your_key")
    client.verify_auth()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

**Connection Issues** - If unable to connect:

* Verify internet connectivity
* Check for firewall restrictions on outgoing connections

## Next Steps

<CardGroup cols={2}>
  <Card title="SDK Examples" icon="code-branch" href="/sdk/sdk-examples">
    See practical examples of API usage with the SDK.
  </Card>

  <Card title="Quickstart Guide" icon="bolt" href="/getting-started/quickstart">
    Follow a step-by-step guide to using the API.
  </Card>
</CardGroup>
