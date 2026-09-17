<template>
  <main class="studio-shell">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark">形</span>
        <div>
          <strong>形镜</strong>
          <span>3D 试衣工作台</span>
        </div>
      </div>
      <div class="topbar-actions">
        <button class="icon-button" title="从照片生成形象" aria-label="从照片生成形象">
          <ScanFace :size="19" />
        </button>
        <button class="secondary-button" type="button" @click="avatar.reset()">
          <RotateCcw :size="17" />
          重置
        </button>
        <button class="primary-button" type="button">
          <Save :size="17" />
          保存形象
        </button>
      </div>
    </header>

    <section class="workspace">
      <aside class="control-panel">
        <nav class="tabs" aria-label="编辑分类">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            <component :is="tab.icon" :size="18" />
            {{ tab.label }}
          </button>
        </nav>

        <div class="controls-scroll">
          <template v-if="activeTab === 'body'">
            <div class="section-heading">
              <div>
                <span>BODY</span>
                <h1>调整身材</h1>
              </div>
              <span class="step-count">01 / 04</span>
            </div>
            <label v-for="control in bodyControls" :key="control.key" class="range-control">
              <span>{{ control.label }}</span>
              <output>{{ Math.round(avatar.body[control.key] * 100) }}</output>
              <input
                v-model.number="avatar.body[control.key]"
                type="range"
                min="0"
                max="1"
                step="0.01"
              />
            </label>
          </template>

          <template v-else-if="activeTab === 'face'">
            <div class="section-heading">
              <div>
                <span>FACE</span>
                <h1>塑造面部</h1>
              </div>
              <span class="step-count">02 / 04</span>
            </div>
            <label v-for="control in faceControls" :key="control.key" class="range-control">
              <span>{{ control.label }}</span>
              <output>{{ Math.round(avatar.face[control.key] * 100) }}</output>
              <input
                v-model.number="avatar.face[control.key]"
                type="range"
                min="0"
                max="1"
                step="0.01"
              />
            </label>
          </template>

          <template v-else-if="activeTab === 'hair'">
            <div class="section-heading">
              <div>
                <span>HAIR</span>
                <h1>选择发型</h1>
              </div>
              <span class="step-count">03 / 04</span>
            </div>
            <div class="option-grid">
              <button
                v-for="hair in hairs"
                :key="hair.id"
                :class="['option-tile', { selected: avatar.appearance.hairId === hair.id }]"
                @click="avatar.appearance.hairId = hair.id"
              >
                <Scissors :size="25" />
                <span>{{ hair.name }}</span>
              </button>
            </div>
            <h2 class="field-title">发色</h2>
            <div class="swatches">
              <button
                v-for="color in hairColors"
                :key="color"
                :style="{ backgroundColor: color }"
                :class="{ selected: avatar.appearance.hairColor === color }"
                :aria-label="`发色 ${color}`"
                @click="avatar.appearance.hairColor = color"
              />
            </div>
          </template>

          <template v-else>
            <div class="section-heading">
              <div>
                <span>WARDROBE</span>
                <h1>搭配服装</h1>
              </div>
              <span class="step-count">04 / 04</span>
            </div>
            <div class="garment-list">
              <button
                v-for="garment in garments"
                :key="garment.id"
                :class="{ selected: avatar.appearance.garmentId === garment.id }"
                @click="avatar.appearance.garmentId = garment.id"
              >
                <Shirt :size="25" />
                <span
                  ><strong>{{ garment.name }}</strong
                  ><small>{{ garment.category }}</small></span
                >
              </button>
            </div>
            <h2 class="field-title">颜色</h2>
            <div class="swatches">
              <button
                v-for="color in garmentColors"
                :key="color"
                :style="{ backgroundColor: color }"
                :class="{ selected: avatar.appearance.garmentColor === color }"
                :aria-label="`服装颜色 ${color}`"
                @click="avatar.appearance.garmentColor = color"
              />
            </div>
          </template>
        </div>
      </aside>

      <section class="stage">
        <AvatarViewport :config="avatar.$state" />
        <div class="status-chip">
          <span></span> 实时预览 · {{ avatar.appearance.garmentSize }} 码
        </div>
      </section>

      <FittingAdvisorPanel />
    </section>
  </main>
</template>

<script setup lang="ts">
import { RotateCcw, Save, ScanFace, Scissors, Shirt, Smile, UserRound } from 'lucide-vue-next'
import { ref } from 'vue'

import AvatarViewport from '../components/AvatarViewport.vue'
import FittingAdvisorPanel from '../components/FittingAdvisorPanel.vue'
import { useAvatarStore } from '../stores/avatar'
import type { BodyParameters, FaceParameters } from '../types/avatar'

const avatar = useAvatarStore()
const activeTab = ref('body')
const tabs = [
  { id: 'body', label: '身材', icon: UserRound },
  { id: 'face', label: '面部', icon: Smile },
  { id: 'hair', label: '发型', icon: Scissors },
  { id: 'outfit', label: '试装', icon: Shirt },
]
const bodyControls: { key: keyof BodyParameters; label: string }[] = [
  { key: 'height', label: '身高' },
  { key: 'weight', label: '胖瘦' },
  { key: 'shoulder', label: '肩宽' },
  { key: 'chest', label: '胸围' },
  { key: 'waist', label: '腰围' },
  { key: 'hip', label: '臀围' },
  { key: 'legLength', label: '腿长' },
]
const faceControls: { key: keyof FaceParameters; label: string }[] = [
  { key: 'faceWidth', label: '脸宽' },
  { key: 'jawWidth', label: '下颌' },
  { key: 'eyeSize', label: '眼睛' },
  { key: 'eyeDistance', label: '眼距' },
  { key: 'noseLength', label: '鼻长' },
  { key: 'mouthWidth', label: '嘴宽' },
]
const hairs = [
  { id: 'hair-short-001', name: '利落短发' },
  { id: 'hair-bob-001', name: '自然短发' },
  { id: 'hair-long-001', name: '柔顺长发' },
  { id: 'hair-pony-001', name: '轻盈马尾' },
]
const garments = [
  { id: 'garment-tee-001', name: '基础圆领上衣', category: '上装' },
  { id: 'garment-shirt-001', name: '通勤衬衫', category: '上装' },
  { id: 'garment-jacket-001', name: '轻量夹克', category: '外套' },
]
const hairColors = ['#241a17', '#563a2c', '#9b6a42', '#1f2428']
const garmentColors = ['#27695c', '#c8553d', '#272c36', '#d6c9ad', '#f4f3ee']
</script>
