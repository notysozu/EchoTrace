import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import * as dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.resolve(__dirname, '../../../.env') });

const s3Client = new S3Client({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || '',
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || ''
  }
});

export async function uploadAudio(buffer: Buffer, key: string): Promise<string> {
  const bucketName = process.env.S3_BUCKET_NAME || 'echotrace-audio';

  try {
    const command = new PutObjectCommand({
      Bucket: bucketName,
      Key: key,
      Body: buffer,
      ContentType: 'audio/mpeg'
    });

    await s3Client.send(command);
    console.log(`[Storage] Successfully uploaded to S3: ${key}`);
    return key;
  } catch (error) {
    console.error(`[Storage] Error uploading ${key} to S3:`, error);
    throw error;
  }
}
