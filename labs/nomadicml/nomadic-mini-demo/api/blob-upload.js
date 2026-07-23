// Client-upload handshake for Vercel Blob — lets the browser upload a video
// DIRECTLY to Blob (bypassing the 4.5 MB serverless request-body limit), while
// the read/write token stays server-side. Password-gated via clientPayload.
const { handleUpload } = require('@vercel/blob/client');

module.exports = async (req, res) => {
  if (req.method !== 'POST') { res.status(405).json({ error: 'POST only' }); return; }
  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    const json = await handleUpload({
      body,
      request: req,
      onBeforeGenerateToken: async (_pathname, clientPayload) => {
        if (!process.env.APP_PASSWORD || clientPayload !== process.env.APP_PASSWORD) {
          throw new Error('unauthorized — wrong demo password');
        }
        return {
          allowedContentTypes: ['video/mp4', 'video/quicktime', 'video/webm', 'video/x-msvideo'],
          maximumSizeInBytes: 150 * 1024 * 1024,
          addRandomSuffix: true,
        };
      },
      onUploadCompleted: async () => { /* no-op; analyze is a separate call */ },
    });
    res.status(200).json(json);
  } catch (e) {
    res.status(400).json({ error: e.message || String(e) });
  }
};
