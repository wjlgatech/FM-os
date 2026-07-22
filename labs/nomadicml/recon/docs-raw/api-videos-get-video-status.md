> ## Documentation Index
> Fetch the complete documentation index at: https://docs.nomadicml.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Get video status

> Return upload and processing status for a video.



## OpenAPI

````yaml /openapi.json get /api/video/{video_id}/status
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
  /api/video/{video_id}/status:
    get:
      tags:
        - Videos
      summary: Get video status
      description: Return upload and processing status for a video.
      operationId: getVideoStatus
      parameters:
        - name: video_id
          in: path
          required: true
          description: Nomadic video identifier.
          schema:
            type: string
      responses:
        '200':
          description: Successful response.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/VideoStatus'
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
    VideoStatus:
      type: object
      properties:
        video_id:
          type: string
        status:
          type: string
        metadata:
          type: object
          additionalProperties: true
      additionalProperties: true
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