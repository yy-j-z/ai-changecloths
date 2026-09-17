export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ToolEvent {
  tool: string
  label: string
  status: 'completed' | 'failed'
  summary: string
}

export interface OutfitAction {
  garmentId: string
  garmentName: string
  size: string
  color: string
  colorHex: string
}

export interface AdvisorResponse {
  conversationId: string
  reply: string
  state: 'needs_input' | 'completed' | 'failed'
  toolEvents: ToolEvent[]
  outfitAction: OutfitAction | null
}
