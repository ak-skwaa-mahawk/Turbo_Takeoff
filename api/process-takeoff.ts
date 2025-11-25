// api/process-takeoff.ts (Edge Function – runs in <2 sec)
import { createClient } from '@supabase/supabase-js'
import Anthropic from '@anthropic-ai/sdk'

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })
const supabase = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_ANON_KEY')!)

export const handler = async (req: Request) => {
  const { fileUrl, userId, trade } = await req.json()

  // 1. Download PDF from Supabase storage → base64
  const { data } = await supabase.storage.from('bids').download(fileUrl)
  const base64 = Buffer.from(await data.arrayBuffer()).toString('base64')

  // 2. Send to Claude 3.5 Sonnet with this prompt (this is the magic)
  const response = await anthropic.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 4096,
    temperature: 0,
    messages: [{
      role: "user",
      content: [
        { type: "text", text: `You are a master ${trade} estimator. Extract every measurable item from these construction plans and specs. Return ONLY valid JSON with this exact structure:
{
  "items": [
    {"description": string, "quantity": number, "unit": "LF|SF|EA|CY", "material_spec": string, "section": string}
  ],
  "notes": string
}
Be ruthless — if it's measurable, count it. Never hallucinate.`},
        { type: "image", image: base64, mime_type: "application/pdf" }
      ]
    }]
  })

  const takeoff = JSON.parse(response.content[0].text)
  
  // 3. Save to DB + return
  const { data: saved } = await supabase.from('takeoffs').insert({ user_id: userId, items: takeoff.items })
  
  return new Response(JSON.stringify(takeoff), { status: 200 })
}