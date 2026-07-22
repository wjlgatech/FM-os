> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Read analysis events

> Read server-sent progress events for a prompt-based analysis started with the analysis start endpoint.



## OpenAPI

````yaml /openapi.json get /api/router/v2/query/events/{stream_id}
openapi: 3.0.3
info:
  title: Nomadic API
  version: 1.0.0
  description: >-
    Curated public REST API for Nomadic video operations. Administrative and
    internal orchestration endpoints are intentionally excluded.
servers:
  - url: https://api-prod.nomadicml.com
    description: Production
  - url: http://localhost:8099
    description: Local development
security: []
tags:
  - name: Authentication
    description: API key verification.
  - name: Uploads
    description: Direct video uploads.
  - name: Videos
    description: Video status, playback URLs, and library operations.
  - name: Analysis
    description: Video analysis.
  - name: Batches
    description: Batch status and result retrieval.
  - name: Folders
    description: Folder creation and lookup.
  - name: Cloud Imports
    description: Asynchronous imports from GCS, S3, and Hugging Face buckets.
  - name: Cloud Integrations
    description: Reusable cloud credential integrations.
  - name: MCAP
    description: MCAP upload and cloud ingest.
  - name: Multi-view
    description: Multi-view video linkage.
  - name: Livestreams
    description: Live-stream session management.
paths:
  /api/router/v2/query/events/{stream_id}:
    get:
      tags:
        - Analysis
      summary: Read analysis events
      description: >-
        Read server-sent progress events for a prompt-based analysis started
        with the analysis start endpoint.
      operationId: getAnalysisEvents
      parameters:
        - name: stream_id
          in: path
          required: true
          description: >-
            Analysis event stream identifier returned by the start analysis
            endpoint.
          schema:
            type: string
        - name: last_id
          in: query
          required: false
          description: Last received SSE event id.
          schema:
            type: string
            default: '0'
      responses:
        '200':
          description: Successful response.
          content:
            text/event-stream:
              schema:
                $ref: '#/components/schemas/SseEventStream'
        '400':
          description: The request was invalid.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '401':
          description: The request is missing valid authentication.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '403':
          description: The authenticated caller does not have access to this resource.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '404':
          description: The requested resource was not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '429':
          description: The request exceeded rate limits.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '500':
          description: The server could not complete the request.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
      security:
        - bearerAuth: []
        - apiKeyAuth: []
components:
  schemas:
    SseEventStream:
      type: string
      description: >-
        Server-sent event stream. Each event is emitted as text/event-stream
        data.
    ErrorResponse:
      type: object
      properties:
        detail:
          description: Error detail returned by FastAPI.
          oneOf:
            - type: string
            - type: object
              additionalProperties: true
        message:
          type: string
        error:
          type: string
      additionalProperties: true
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: API key
      description: 'Use `Authorization: Bearer <NOMADIC_API_KEY>`.'
    apiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: Alternative API-key header accepted by parts of the API.

````