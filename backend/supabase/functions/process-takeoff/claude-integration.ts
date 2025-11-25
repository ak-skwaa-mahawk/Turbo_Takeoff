// backend/supabase/functions/process-takeoff/claude-integration.ts
// Deno edge function for processing construction takeoffs with Claude

import Anthropic from "npm:@anthropic-ai/sdk@0.32.1";

interface TakeoffRequest {
  fileUrl: string;
  tradeType: string;
  userPreferences?: {
    manufacturerPriorities?: string[];
    unitTypes?: string[];
  };
}

interface TakeoffItem {
  description: string;
  quantity: number;
  unit: string;
  material?: string;
  manufacturer?: string;
  specification?: string;
  location?: string;
  notes?: string;
}

interface TakeoffResponse {
  items: TakeoffItem[];
  summary: {
    totalLineItems: number;
    tradeType: string;
    documentPages: number;
    confidence: number;
  };
  warnings: string[];
}

export async function processTakeoffWithClaude(
  request: TakeoffRequest
): Promise<TakeoffResponse> {
  const anthropic = new Anthropic({
    apiKey: Deno.env.get("ANTHROPIC_API_KEY"),
  });

  // Download PDF from Supabase storage
  const pdfResponse = await fetch(request.fileUrl);
  const pdfBuffer = await pdfResponse.arrayBuffer();
  const base64Pdf = btoa(String.fromCharCode(...new Uint8Array(pdfBuffer)));

  // Construct the prompt based on trade type
  const tradePrompts = {
    waterproofing: `You are analyzing construction plans for a WATERPROOFING takeoff. Extract:
- Linear feet of joints (expansion, control, construction, etc.)
- Square feet of deck coatings, membranes, EIFS
- Each count of penetrations, drains, terminations
- Manufacturer callouts (Tremco, Sika, BASF, etc.)
- Spec section references`,

    electrical: `You are analyzing construction plans for an ELECTRICAL takeoff. Extract:
- Linear feet of conduit runs by size
- Each count of outlets, switches, panels, fixtures
- Wire quantities by gauge and type
- Equipment specifications
- Panel schedules`,

    plumbing: `You are analyzing construction plans for a PLUMBING takeoff. Extract:
- Linear feet of piping by size and material
- Each count of fixtures, valves, fittings
- Water heater/equipment specifications
- Drain/vent system quantities`,

    hvac: `You are analyzing construction plans for an HVAC takeoff. Extract:
- Each count of equipment (units, fans, pumps)
- Linear feet of ductwork by size
- Supply/return grille quantities
- Refrigerant line sets
- Control system components`,

    general: `You are analyzing construction plans for a takeoff. Extract ALL measurable quantities:
- Linear measurements (feet, meters)
- Area measurements (square feet, square meters)
- Count items (each)
- Volume measurements (cubic yards)
- Material specifications and manufacturers`,
  };

  const prompt =
    tradePrompts[request.tradeType as keyof typeof tradePrompts] ||
    tradePrompts.general;

  const systemPrompt = `You are an expert construction estimator with deep knowledge of reading blueprints, specifications, and construction documents. Your task is to perform a detailed quantity takeoff.

CRITICAL INSTRUCTIONS:
1. Extract EVERY measurable quantity from the plans
2. Organize by CSI division/trade section
3. Include manufacturer callouts when specified
4. Note specification section references
5. Flag any unclear or ambiguous quantities
6. Use standard units: LF (linear feet), SF (square feet), EA (each), CY (cubic yards)

${prompt}

OUTPUT FORMAT (JSON only, no other text):
{
  "items": [
    {
      "description": "Expansion Joint Sealant - Horizontal",
      "quantity": 450,
      "unit": "LF",
      "material": "Two-part polyurethane sealant",
      "manufacturer": "Tremco Dymonic FC",
      "specification": "07920 - 2.3.A",
      "location": "Level 2 deck",
      "notes": "1/2\" x 1/2\" joint"
    }
  ],
  "warnings": ["Unable to read dimension on sheet A-3.2", "Spec callout unclear on page 47"]
}

Be thorough. A missed quantity costs money.`;

  try {
    const message = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 16000,
      temperature: 0.2, // Low temperature for consistency
      system: systemPrompt,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "document",
              source: {
                type: "base64",
                media_type: "application/pdf",
                data: base64Pdf,
              },
            },
            {
              type: "text",
              text: `Perform a complete quantity takeoff for ${request.tradeType} work. Be extremely detailed.`,
            },
          ],
        },
      ],
    });

    // Extract JSON from response
    const responseText =
      message.content.find((block) => block.type === "text")?.text || "";

    // Parse JSON (handle potential markdown code blocks)
    let jsonText = responseText.trim();
    if (jsonText.startsWith("```json")) {
      jsonText = jsonText
        .replace(/^```json\s*/, "")
        .replace(/\s*```$/, "")
        .trim();
    } else if (jsonText.startsWith("```")) {
      jsonText = jsonText.replace(/^```\s*/, "").replace(/\s*```$/, "").trim();
    }

    const parsed = JSON.parse(jsonText);

    // Apply user preferences (manufacturer priorities)
    if (request.userPreferences?.manufacturerPriorities) {
      parsed.items = parsed.items.map((item: TakeoffItem) => {
        // If manufacturer not specified in plans, suggest from priority list
        if (!item.manufacturer && item.material) {
          item.manufacturer = request.userPreferences.manufacturerPriorities[0];
          item.notes = item.notes
            ? `${item.notes} | Suggested manufacturer from preferences`
            : "Suggested manufacturer from preferences";
        }
        return item;
      });
    }

    // Calculate confidence score based on warnings
    const confidence = Math.max(70, 100 - parsed.warnings.length * 5);

    return {
      items: parsed.items || [],
      summary: {
        totalLineItems: parsed.items?.length || 0,
        tradeType: request.tradeType,
        documentPages: 0, // TODO: extract from PDF metadata
        confidence,
      },
      warnings: parsed.warnings || [],
    };
  } catch (error) {
    console.error("Claude API error:", error);
    throw new Error(`Failed to process takeoff: ${error.message}`);
  }
}

// Example usage in Supabase edge function
Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  }

  try {
    const { fileUrl, tradeType, userPreferences } = await req.json();

    if (!fileUrl || !tradeType) {
      return new Response(
        JSON.stringify({ error: "Missing fileUrl or tradeType" }),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        }
      );
    }

    const result = await processTakeoffWithClaude({
      fileUrl,
      tradeType,
      userPreferences,
    });

    return new Response(JSON.stringify(result), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  } catch (error) {
    console.error("Error processing takeoff:", error);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }
});