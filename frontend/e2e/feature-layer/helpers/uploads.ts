type UploadPayload = {
  name: string;
  mimeType: string;
  buffer: Buffer;
};

export function makeUploadFile(name: string, content: string): UploadPayload {
  return {
    name,
    mimeType: 'application/pdf',
    buffer: Buffer.from(content, 'utf-8'),
  };
}
