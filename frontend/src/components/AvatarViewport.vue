<template>
  <div ref="host" class="viewport" aria-label="3D 数字人预览">
    <div class="view-hint">拖拽旋转 · 滚轮缩放</div>
  </div>
</template>

<script setup lang="ts">
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import * as THREE from 'three'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

import type { AvatarConfig } from '../types/avatar'

const props = defineProps<{ config: AvatarConfig }>()
const host = ref<HTMLDivElement>()

let renderer: THREE.WebGLRenderer | undefined
let controls: OrbitControls | undefined
let observer: ResizeObserver | undefined
let frameId = 0

const bodyParts: Record<string, THREE.Mesh> = {}
const materials: Record<string, THREE.MeshStandardMaterial> = {}

function createMesh(
  name: string,
  geometry: THREE.BufferGeometry,
  material: THREE.Material,
  position: [number, number, number],
): THREE.Mesh {
  const mesh = new THREE.Mesh(geometry, material)
  mesh.name = name
  mesh.position.set(...position)
  mesh.castShadow = true
  mesh.receiveShadow = true
  bodyParts[name] = mesh
  return mesh
}

function applyConfig(config: AvatarConfig) {
  const weightScale = 0.78 + config.body.weight * 0.48
  const heightScale = 0.9 + config.body.height * 0.2
  const shoulderScale = 0.85 + config.body.shoulder * 0.35
  const hipScale = 0.85 + config.body.hip * 0.32
  const faceScale = 0.86 + config.face.faceWidth * 0.28

  bodyParts.torso?.scale.set(weightScale * shoulderScale, heightScale, weightScale)
  bodyParts.shirt?.scale.set(weightScale * shoulderScale * 1.04, heightScale, weightScale * 1.04)
  bodyParts.hips?.scale.set(weightScale * hipScale, 1, weightScale)
  bodyParts.head?.scale.set(faceScale, 1.02, 1)
  bodyParts.hair?.scale.set(faceScale * 1.04, 1.05, 1.04)

  const legLength = 0.88 + config.body.legLength * 0.24
  bodyParts.leftLeg?.scale.set(1, legLength, 1)
  bodyParts.rightLeg?.scale.set(1, legLength, 1)

  materials.skin?.color.set(config.appearance.skinColor)
  materials.hair?.color.set(config.appearance.hairColor)
  materials.garment?.color.set(config.appearance.garmentColor)
}

onMounted(() => {
  if (!host.value) return

  const scene = new THREE.Scene()
  scene.background = new THREE.Color('#e8ece6')

  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100)
  camera.position.set(3.4, 2.3, 5.4)

  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.shadowMap.enabled = true
  renderer.outputColorSpace = THREE.SRGBColorSpace
  host.value.prepend(renderer.domElement)

  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.target.set(0, 1.45, 0)
  controls.minDistance = 3
  controls.maxDistance = 8

  materials.skin = new THREE.MeshStandardMaterial({ color: '#d7a17d', roughness: 0.72 })
  materials.hair = new THREE.MeshStandardMaterial({ color: '#241a17', roughness: 0.9 })
  materials.garment = new THREE.MeshStandardMaterial({ color: '#27695c', roughness: 0.62 })
  const trouser = new THREE.MeshStandardMaterial({ color: '#252a2d', roughness: 0.8 })

  const avatar = new THREE.Group()
  avatar.add(createMesh('head', new THREE.SphereGeometry(0.3, 36, 24), materials.skin, [0, 2.72, 0]))
  avatar.add(
    createMesh('hair', new THREE.SphereGeometry(0.315, 36, 20, 0, Math.PI * 2, 0, 1.8), materials.hair, [0, 2.78, -0.005]),
  )
  avatar.add(createMesh('torso', new THREE.CapsuleGeometry(0.43, 0.68, 8, 24), materials.skin, [0, 1.92, 0]))
  avatar.add(createMesh('shirt', new THREE.CapsuleGeometry(0.45, 0.66, 8, 24), materials.garment, [0, 1.94, 0]))
  avatar.add(createMesh('hips', new THREE.CapsuleGeometry(0.4, 0.2, 8, 24), trouser, [0, 1.28, 0]))
  avatar.add(createMesh('leftLeg', new THREE.CapsuleGeometry(0.16, 0.78, 8, 20), trouser, [-0.21, 0.65, 0]))
  avatar.add(createMesh('rightLeg', new THREE.CapsuleGeometry(0.16, 0.78, 8, 20), trouser, [0.21, 0.65, 0]))
  avatar.add(createMesh('leftArm', new THREE.CapsuleGeometry(0.12, 0.74, 8, 18), materials.skin, [-0.62, 1.9, 0]))
  avatar.add(createMesh('rightArm', new THREE.CapsuleGeometry(0.12, 0.74, 8, 18), materials.skin, [0.62, 1.9, 0]))
  scene.add(avatar)

  const floor = new THREE.Mesh(
    new THREE.CircleGeometry(2.1, 64),
    new THREE.MeshStandardMaterial({ color: '#f8f9f6', roughness: 0.95 }),
  )
  floor.rotation.x = -Math.PI / 2
  floor.receiveShadow = true
  scene.add(floor)

  scene.add(new THREE.HemisphereLight('#ffffff', '#708078', 2.3))
  const key = new THREE.DirectionalLight('#fff8eb', 4.2)
  key.position.set(3, 6, 4)
  key.castShadow = true
  scene.add(key)
  const rim = new THREE.DirectionalLight('#bcd9d4', 2)
  rim.position.set(-4, 3, -3)
  scene.add(rim)

  applyConfig(props.config)

  observer = new ResizeObserver(([entry]) => {
    const { width, height } = entry.contentRect
    if (!renderer || height === 0) return
    renderer.setSize(width, height, false)
    camera.aspect = width / height
    camera.updateProjectionMatrix()
  })
  observer.observe(host.value)

  const render = () => {
    controls?.update()
    renderer?.render(scene, camera)
    frameId = requestAnimationFrame(render)
  }
  render()
})

watch(() => props.config, applyConfig, { deep: true })

onBeforeUnmount(() => {
  cancelAnimationFrame(frameId)
  observer?.disconnect()
  controls?.dispose()
  renderer?.dispose()
})
</script>

