> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Create signed URLs in bulk

> Create short-lived signed playback URLs for multiple videos.



## OpenAPI

````yaml /openapi.json post /api/video/signed-urls
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
  /api/video/signed-urls:
    post:
      tags:
        - Videos
      summary: Create signed URLs in bulk
      description: Create short-lived signed playback URLs for multiple videos.
      operationId: createSignedVideoUrls
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BulkSignedUrlRequest'
      responses:
        '200':
          description: Successful response.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BulkSignedUrlResponse'
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
    BulkSignedUrlRequest:
      type: object
      properties:
        requests:
          type: array
          maxItems: 50
          items:
            $ref: '#/components/schemas/BulkSignedUrlRequestItem'
      required:
        - requests
    BulkSignedUrlResponse:
      type: object
      properties:
        results:
          type: object
          description: Map of request_id to a signed URL result or per-item error.
          additionalProperties:
            oneOf:
              - $ref: '#/components/schemas/BulkSignedUrlSuccess'
              - $ref: '#/components/schemas/BulkSignedUrlError'
      required:
        - results
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
    BulkSignedUrlRequestItem:
      type: object
      properties:
        request_id:
          type: string
        video_id:
          type: string
        path:
          type: string
        expires_in:
          type: integer
          default: 900
          minimum: 60
          maximum: 3600
        method:
          type: string
          enum:
            - GET
            - HEAD
          default: GET
        share_token:
          type: string
        allow_sample:
          type: boolean
          default: false
        batch_id:
          type: string
      required:
        - request_id
        - video_id
    BulkSignedUrlSuccess:
      type: object
      properties:
        ok:
          type: boolean
          enum:
            - true
        url:
          type: string
          format: uri
        expires_at:
          type: string
        method:
          type: string
          enum:
            - GET
            - HEAD
      required:
        - ok
        - url
        - expires_at
        - method
      additionalProperties: true
    BulkSignedUrlError:
      type: object
      properties:
        ok:
          type: boolean
          enum:
            - false
        error:
          oneOf:
            - type: string
            - type: object
              additionalProperties: true
        status:
          type: integer
      required:
        - ok
        - error
        - status
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