import OpenAI from 'openai';
import * as dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.resolve(__dirname, '../../../.env') });

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export type PerspectiveScripts = {
  narrator: string;
  eyewitness: string;
  historian: string;
  opposition: string;
};

export async function generateScripts(eventName: string, summaryText: string, eraLabel: string): Promise<PerspectiveScripts> {
  const prompt = `
You are a historical audio drama pipeline.
Write four short, highly immersive scripts (under 60 words each) for the historical event: "${eventName}" during the era: "${eraLabel}".
Context: ${summaryText}

You must write exactly 4 scripts from these perspectives:
1. "narrator": A cinematic, objective voice setting the scene.
2. "eyewitness": A subjective first-person account from someone who was there.
3. "historian": An analytical retrospective view, explaining the impact.
4. "opposition": A skeptical, rival, or opposing view on the event.

Return a raw JSON object (NO markdown formatting, NO \`\`\`json) with these exactly four keys: narrator, eyewitness, historian, opposition.
`.trim();

  try {
    const response = await openai.chat.completions.create({
      model: process.env.OPENAI_MODEL || "gpt-4o",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.7,
      response_format: { type: "json_object" }
    });

    const content = response.choices[0].message.content;
    if (!content) throw new Error("No content returned from OpenAI");

    return JSON.parse(content) as PerspectiveScripts;
  } catch (error) {
    console.error("[OpenAI] Error generating scripts:", error);
    throw error;
  }
}
