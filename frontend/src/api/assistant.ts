import request from './request'
import type { AdvisorResponse, ChatMessage } from '../types/assistant'

interface AdvisorPayload {
  conversation_id?: string
  message: string
  history: ChatMessage[]
  user_height_cm: number
  user_weight_kg: number
}

interface RawAdvisorResponse {
  conversation_id: string
  reply: string
  state: AdvisorResponse['state']
  tool_events: Array<{
    tool: string
    label: string
    status: 'completed' | 'failed'
    summary: string
  }>
  outfit_action: null | {
    garment_id: string
    garment_name: string
    size: string
    color: string
    color_hex: string
  }
}

export async function askFittingAdvisor(payload: AdvisorPayload): Promise<AdvisorResponse> {
  const data = await request.post<RawAdvisorResponse, RawAdvisorResponse>(
    '/assistant/chat',
    payload,
  )
  return {
    conversationId: data.conversation_id,
    reply: data.reply,
    state: data.state,
    toolEvents: data.tool_events,
    outfitAction: data.outfit_action
      ? {
          garmentId: data.outfit_action.garment_id,
          garmentName: data.outfit_action.garment_name,
          size: data.outfit_action.size,
          color: data.outfit_action.color,
          colorHex: data.outfit_action.color_hex,
        }
      : null,
  }
}
