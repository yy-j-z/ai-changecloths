<template>
  <aside class="advisor-panel">
    <header class="advisor-header">
      <div class="advisor-title">
        <span class="advisor-icon"><Sparkles :size="17" /></span>
        <div>
          <strong>穿搭顾问</strong>
          <span><i></i> 智能体在线</span>
        </div>
      </div>
      <button
        class="advisor-clear"
        type="button"
        title="清空对话"
        aria-label="清空对话"
        @click="clearChat"
      >
        <Trash2 :size="16" />
      </button>
    </header>

    <div ref="messageList" class="advisor-messages" aria-live="polite">
      <article
        v-for="(message, index) in messages"
        :key="index"
        :class="['chat-message', message.role]"
      >
        <p>{{ message.content }}</p>
        <div v-if="message.events?.length" class="tool-events">
          <div v-for="event in message.events" :key="event.tool">
            <CircleCheck :size="14" />
            <span
              ><strong>{{ event.label }}</strong
              >{{ event.summary }}</span
            >
          </div>
        </div>
      </article>

      <div v-if="loading" class="agent-thinking">
        <LoaderCircle :size="15" />
        正在调用搭配工具
      </div>
    </div>

    <div class="advisor-suggestions">
      <button
        v-for="suggestion in suggestions"
        :key="suggestion"
        type="button"
        @click="submit(suggestion)"
      >
        {{ suggestion }}
      </button>
    </div>

    <form class="advisor-input" @submit.prevent="submit(input)">
      <textarea
        v-model="input"
        rows="2"
        placeholder="说说场景、风格和预算"
        @keydown.enter.exact.prevent="submit(input)"
      />
      <button type="submit" :disabled="loading || !input.trim()" aria-label="发送">
        <Send :size="17" />
      </button>
    </form>
  </aside>
</template>

<script setup lang="ts">
import { CircleCheck, LoaderCircle, Send, Sparkles, Trash2 } from 'lucide-vue-next'
import { nextTick, ref } from 'vue'

import { askFittingAdvisor } from '../api/assistant'
import { useAvatarStore } from '../stores/avatar'
import type { ChatMessage, ToolEvent } from '../types/assistant'

interface DisplayMessage extends ChatMessage {
  events?: ToolEvent[]
}

const avatar = useAvatarStore()
const input = ref('')
const loading = ref(false)
const conversationId = ref<string>()
const messageList = ref<HTMLDivElement>()
const messages = ref<DisplayMessage[]>([
  {
    role: 'assistant',
    content: '告诉我穿着场景、喜欢的风格和预算，我会查询商品并直接为数字人试穿。',
  },
])
const suggestions = ['面试，正式但不要全黑，预算800', '校园日常，简约舒适，预算300']

async function scrollToLatest() {
  await nextTick()
  messageList.value?.scrollTo({ top: messageList.value.scrollHeight, behavior: 'smooth' })
}

async function submit(value: string) {
  const content = value.trim()
  if (!content || loading.value) return

  const history = messages.value.map(({ role, content: text }) => ({ role, content: text }))
  messages.value.push({ role: 'user', content })
  input.value = ''
  loading.value = true
  await scrollToLatest()

  try {
    const result = await askFittingAdvisor({
      conversation_id: conversationId.value,
      message: content,
      history,
      user_height_cm: 155 + avatar.body.height * 35,
      user_weight_kg: 45 + avatar.body.weight * 55,
    })
    conversationId.value = result.conversationId
    messages.value.push({ role: 'assistant', content: result.reply, events: result.toolEvents })
    if (result.outfitAction) {
      avatar.applyOutfit(
        result.outfitAction.garmentId,
        result.outfitAction.colorHex,
        result.outfitAction.size,
      )
    }
  } catch (error) {
    const detail = error instanceof Error ? error.message : '服务暂时不可用'
    messages.value.push({ role: 'assistant', content: `没有完成这次搭配：${detail}` })
  } finally {
    loading.value = false
    await scrollToLatest()
  }
}

function clearChat() {
  conversationId.value = undefined
  messages.value = [{ role: 'assistant', content: '对话已清空。告诉我下一次需要搭配的场景吧。' }]
}
</script>
