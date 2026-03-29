import { Client } from 'pg';
import * as dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.resolve(__dirname, '../../../.env') });

// Construct the postgres URI. In local Docker, this usually runs on localhost if the worker is external,
// But since we use docker network aliases in standard prod, we fall back to standard parsing.
// Strip asyncpg dialect from the URL for the Node.js native client
let dbUrl = process.env.DATABASE_URL || 'postgresql://echotrace:echotrace_secret@localhost:5432/echotrace';
dbUrl = dbUrl.replace('+asyncpg', '');

const pgClient = new Client({
  connectionString: dbUrl,
});

pgClient.connect().catch(e => console.error("[DB] Failed to connect:", e));

export async function saveAudioRecord(
  eventId: string, 
  perspectiveType: string, 
  s3Key: string,
  durationSeconds: number = 60
) {
  const query = `
    INSERT INTO audio_files (id, event_id, perspective_type, s3_key, format, duration_seconds, is_active)
    VALUES (gen_random_uuid(), $1, $2, $3, 'mp3', $4, true)
    RETURNING id;
  `;
  const values = [eventId, perspectiveType, s3Key, durationSeconds];
  
  try {
    const res = await pgClient.query(query, values);
    return res.rows[0].id;
  } catch (error) {
    console.error("[DB] Error saving audio record:", error);
    throw error;
  }
}

export async function publishEvent(eventId: string) {
  const query = `UPDATE events SET is_published = true WHERE id = $1`;
  await pgClient.query(query, [eventId]);
}
