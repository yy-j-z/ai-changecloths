import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'

import { useAvatarStore } from './avatar'

describe('avatar store', () => {
  beforeEach(() => setActivePinia(createPinia()))

  it('restores defaults after edits', () => {
    const avatar = useAvatarStore()
    avatar.body.weight = 0.9

    avatar.reset()

    expect(avatar.body.weight).toBe(0.5)
  })
})
