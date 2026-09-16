export interface BodyParameters {
  height: number
  weight: number
  shoulder: number
  chest: number
  waist: number
  hip: number
  legLength: number
}

export interface FaceParameters {
  faceWidth: number
  jawWidth: number
  eyeSize: number
  eyeDistance: number
  noseLength: number
  mouthWidth: number
}

export interface AppearanceParameters {
  skinColor: string
  hairId: string
  hairColor: string
  garmentId: string
  garmentColor: string
}

export interface AvatarConfig {
  body: BodyParameters
  face: FaceParameters
  appearance: AppearanceParameters
}

