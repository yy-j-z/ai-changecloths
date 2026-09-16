import { defineStore } from 'pinia'

import type { AvatarConfig } from '../types/avatar'

export const DEFAULT_AVATAR: AvatarConfig = {
  body: {
    height: 0.5,
    weight: 0.5,
    shoulder: 0.5,
    chest: 0.5,
    waist: 0.5,
    hip: 0.5,
    legLength: 0.5,
  },
  face: {
    faceWidth: 0.5,
    jawWidth: 0.5,
    eyeSize: 0.5,
    eyeDistance: 0.5,
    noseLength: 0.5,
    mouthWidth: 0.5,
  },
  appearance: {
    skinColor: '#d7a17d',
    hairId: 'hair-short-001',
    hairColor: '#241a17',
    garmentId: 'garment-tee-001',
    garmentColor: '#27695c',
  },
}

function cloneDefault(): AvatarConfig {
  return JSON.parse(JSON.stringify(DEFAULT_AVATAR)) as AvatarConfig
}

export const useAvatarStore = defineStore('avatar', {
  state: (): AvatarConfig => cloneDefault(),
  actions: {
    reset() {
      Object.assign(this, cloneDefault())
    },
  },
})

