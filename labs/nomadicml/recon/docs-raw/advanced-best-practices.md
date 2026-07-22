> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Best Practices

> Optimize your usage of Nomadic and get the most from your video analysis

# Best Practices

This guide provides recommendations and best practices to help you get the most out of Nomadic's motion analysis platform.

## Video Capture Guidelines

The quality of your analysis begins with the quality of your video input. Follow these guidelines for optimal results:

### Camera Placement

* **Primary View**: Mount the camera with optimal perspective for your use case
* **Height**: Position at appropriate level for capturing motion (varies by application)
* **Angle**: Adjust angle to capture the area of interest
* **Clear View**: Ensure the camera has an unobstructed view of the scene

<img src="https://mintlify.s3.us-west-1.amazonaws.com/nomadicmlinc/images/camera-placement.png" alt="Camera Placement" />

### Video Quality

* **Resolution**: Minimum 720p (1280×720), recommended 1080p (1920×1080)
* **Frame Rate**: Minimum 24 fps, recommended 30 fps
* **Bitrate**: Minimum 4 Mbps, recommended 8 Mbps
* **Format**: MP4 with H.264 encoding works best
* **Lighting**: Ensure adequate lighting for clear visibility
* **Weather**: Be aware that heavy rain, snow, or fog can affect analysis accuracy

### Recording Length

* **Optimal Duration**: 5-20 minutes per video for best performance
* **Split Longer Sessions**: For recordings over 30 minutes, consider splitting into multiple videos
* **Context**: Include enough time before and after key events for proper context

## Data Management

Effective data management ensures you can access and use your analysis effectively.

### Video Organization

* **Consistent Naming**: Use a consistent naming scheme for videos (e.g., `YYYY-MM-DD_Operator_Location.mp4`)
* **Metadata**: Add relevant metadata when uploading (operator, equipment, location, etc.)
* **Tagging**: Use tags to categorize videos by purpose, location, or scenario
* **Archiving**: Develop a policy for archiving older videos to manage storage

### Analysis Retention

Consider how long you need to retain analysis data:

* **Short-term (30 days)**: Recent training sessions or evaluations
* **Medium-term (90 days)**: Trend analysis and pattern recognition
* **Long-term (1+ years)**: Historical comparisons and compliance documentation

## API Usage Optimization

When working with the Nomadic API, follow these practices for optimal performance and reliability.

### Rate Limiting

* **Respect Limits**: Stay within the published rate limits (60 requests/minute, 10,000/day)
* **Batch Operations**: Combine multiple operations into fewer API calls when possible
* **Implement Backoff**: Use exponential backoff when receiving rate limit errors
* **Monitor Usage**: Track your API usage to avoid unexpected throttling

### Efficient Requests

* **Pagination**: Use pagination parameters for large result sets
* **Filtering**: Apply server-side filters to reduce data transfer
* **Field Selection**: Request only the fields you need
* **Compression**: Use gzip compression for larger responses

```python theme={null}
# Example of efficient API usage
import requests

API_BASE = "https://api-prod.nomadicml.com/api"
API_KEY = "your_api_key"

headers = {
    "X-API-Key": API_KEY,
    "Accept-Encoding": "gzip"  # Request compression
}

# Use pagination and filters
params = {
    "limit": 100,  # Page size
    "offset": 0,   # Starting point
    "event_type": "Motion Anomaly",  # Filter by type
    "fields": "video_id,time,type,severity,description"  # Select only needed fields
}

all_events = []
while True:
    response = requests.get(
        f"{API_BASE}/events",
        headers=headers,
        params=params
    )
    
    data = response.json()
    events = data["events"]
    
    if not events:
        break
        
    all_events.extend(events)
    params["offset"] += params["limit"]  # Move to next page
```

### Caching

Implement client-side caching for frequently accessed data:

* **TTL-based Caching**: Cache responses with appropriate time-to-live values
* **Conditional Requests**: Use etags or last-modified headers for validation
* **Local Storage**: Store reference data locally (e.g., event types, DMV rules)

## SDK Best Practices

When using the Nomadic Python SDK, follow these recommendations:

### Environment Setup

* **Virtual Environments**: Use virtual environments to manage dependencies
* **Version Pinning**: Pin the SDK version in your requirements.txt file
* **Configuration Management**: Use environment variables or secure configuration files for API keys

```bash theme={null}
# Example environment setup
python -m venv nomadic-env
source nomadic-env/bin/activate  # Or nomadic-env\Scripts\activate on Windows
pip install nomadic==0.1.0
```

### Error Handling

Implement robust error handling:

```python theme={null}
from nomadic import NomadicAI
from nomadicml.exceptions import (
    AuthenticationError,
    VideoUploadError,
    AnalysisError,
    NomadicError
)

try:
    client = NomadicAI(api_key="your_api_key")
    response = client.upload(url)
    response = client.analyze(
        response['video_id'],
        prompt="Find all instances of ego vehicle straddling two lanes",
    )

    
except AuthenticationError:
    # Handle authentication issues
    print("Authentication failed - check your API key")
except VideoUploadError as e:
    # Handle upload-specific errors
    print(f"Upload failed: {e}")
except AnalysisError as e:
    # Handle analysis-specific errors
    print(f"Analysis failed: {e}")
except NomadicError as e:
    # Handle all other SDK errors
    print(f"An error occurred: {e}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")
```

## Analysis Interpretation

Getting the most from your analysis requires proper interpretation of the results.

### Context Matters

* **Environmental Factors**: Consider weather, lighting, and environmental conditions
* **Equipment Limitations**: Account for equipment capabilities and characteristics
* **Operation Purpose**: Interpret events in the context of the operational purpose (training, testing, monitoring, etc.)

### Severity Assessment

When evaluating event severity:

* **Low Severity**: Opportunities for improvement, not immediate safety concerns
* **Medium Severity**: Notable issues that should be addressed
* **High Severity**: Critical safety concerns requiring immediate attention

### Trend Analysis

Look beyond individual events to identify patterns:

* **Frequency Analysis**: Track event frequency over time
* **Location Patterns**: Identify problematic locations or scenarios
* **Operator Comparison**: Compare performance across different operators
* **Before/After**: Measure the impact of training or interventions

## Performance Optimization

For systems processing large volumes of videos, consider these optimization strategies:

### Batch Processing

* Process videos in batches during off-peak hours
* Use background workers for upload and analysis tasks
* Implement queuing systems for large workloads

### Resource Management

* Compress videos before upload to reduce bandwidth
* Clean up temporary files after processing
* Implement TTL (time-to-live) policies for stored videos

## Security Best Practices

Protect your data and access with these security measures:

### API Key Management

* **Rotation**: Rotate API keys regularly (every 90 days recommended)
* **Scope Limitation**: Use the minimum required permissions
* **Secure Storage**: Store API keys in secure credential stores, not in code
* **Monitoring**: Monitor API key usage for unusual patterns

### Data Security

* **Encryption**: Ensure data is encrypted in transit and at rest
* **Access Control**: Implement proper access controls for videos and analysis data
* **Data Minimization**: Only store the data you need
* **Retention Policy**: Implement data retention and deletion policies

### Audit Trail

Maintain an audit trail of system activities:

* Log all video uploads and deletions
* Track who accessed analysis results
* Record API key creation and revocation
* Monitor for suspicious activity

## Next Steps

Now that you understand the best practices, explore these advanced topics:

<CardGroup cols={2}>
  <Card title="API Reference" icon="book-open" href="/advanced/authentication">
    Detailed API documentation
  </Card>

  <Card title="SDK Examples" icon="code-branch" href="/sdk/sdk-examples">
    See practical examples of SDK usage.
  </Card>
</CardGroup>
