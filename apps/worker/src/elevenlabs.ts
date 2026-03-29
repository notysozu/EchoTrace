import { ElevenLabsClient } from "elevenlabs";
import * as dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.resolve(__dirname, '../../../.env') });

const client = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY
});

// Map generated perspective roles to specific ElevenLabs voice IDs
// (Keys should match the PerspectiveScripts object from openai.ts)
const VOICE_MAP: Record<string, string> = {
  narrator: 'JBFqnCBcs6BaNtIGwgZ1', // Example: George (Deep/Objective)
  eyewitness: 'EXAVITQu4vr4xnSDxMaL', // Example: Bella (Emotional)
  historian: 'TxGEqnHWrfWFTfGW9XjX', // Example: Josh (Analytical)
  opposition: 'VR6AewLTigWG4xSOukaG', // Example: Arnold (Skeptical/Gruff)
};

export async function generateAudio(perspective: string, text: string): Promise<Buffer> {
  try {
    const voiceId = VOICE_MAP[perspective] || VOICE_MAP['narrator'];
    
    const audioStream = await client.textToSpeech.convert(voiceId, {
      output_format: "mp3_44100_128",
      text: text,
      model_id: "eleven_turbo_v2"
    });

    const chunks: Buffer[] = [];
    for await (const chunk of audioStream) {
      chunks.push(chunk);
    }
    return Buffer.concat(chunks);
  } catch (error) {
    console.error(`[ElevenLabs] Error generating TTS for ${perspective}:`, error);
    throw error;
  }
}
