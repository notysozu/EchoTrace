import { exec } from 'child_process';
import util from 'util';
import fs from 'fs/promises';
import path from 'path';

const execAsync = util.promisify(exec);

export async function mixAudioFiles(
  voiceBuffer: Buffer, 
  ambientS3KeyOrPath: string | null
): Promise<Buffer> {
  const tmpVoice = `/tmp/voice_${Date.now()}.mp3`;
  const tmpOutput = `/tmp/mixed_${Date.now()}.mp3`;
  
  try {
    // Write the raw TTS buffer to a temporary file
    await fs.writeFile(tmpVoice, voiceBuffer);

    // If no ambient track is provided, just return the voice buffer
    if (!ambientS3KeyOrPath) {
       await fs.unlink(tmpVoice).catch(() => {});
       return voiceBuffer; 
    }

    // Determine ambient file path (mocked for MVP to use a local default if S3 isn't available)
    // Realistically this would download from S3 first. We assume it's pre-downloaded or local.
    const ambientPath = path.resolve(__dirname, '../../web/public/sounds/ambient.mp3');
    
    // Check if the mock ambient track exists, if not just return voice
    try {
      await fs.access(ambientPath);
    } catch {
      console.warn(`[FFmpeg] Ambient track not found at ${ambientPath}, returning unmixed voice`);
      await fs.unlink(tmpVoice).catch(() => {});
      return voiceBuffer;
    }

    // FFmpeg command: Mix the two files. 
    // -stream_loop -1 loops the ambient track. 
    // amix=inputs=2:duration=first makes sure the output ends when the voice ends.
    // volume=0.3 drops the ambient track volume.
    const ffmpegCmd = `ffmpeg -y -i ${tmpVoice} -stream_loop -1 -i ${ambientPath} -filter_complex "[1:a]volume=0.2[a1];[0:a][a1]amix=inputs=2:duration=first:dropout_transition=2" -c:a libmp3lame -q:a 4 ${tmpOutput}`;
    
    console.log(`[FFmpeg] Mixing audio:`, ffmpegCmd);
    await execAsync(ffmpegCmd);

    const mixedBuffer = await fs.readFile(tmpOutput);
    return mixedBuffer;
  } catch (error) {
    console.error("[FFmpeg] Mixing error:", error);
    throw error;
  } finally {
    // Cleanup temporary files
    await fs.unlink(tmpVoice).catch(() => {});
    await fs.unlink(tmpOutput).catch(() => {});
  }
}
