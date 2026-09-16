from pydantic import BaseModel, Field

Normalized = float


class BodyParameters(BaseModel):
    height: Normalized = Field(default=0.5, ge=0, le=1)
    weight: Normalized = Field(default=0.5, ge=0, le=1)
    shoulder: Normalized = Field(default=0.5, ge=0, le=1)
    chest: Normalized = Field(default=0.5, ge=0, le=1)
    waist: Normalized = Field(default=0.5, ge=0, le=1)
    hip: Normalized = Field(default=0.5, ge=0, le=1)
    leg_length: Normalized = Field(default=0.5, ge=0, le=1)


class FaceParameters(BaseModel):
    face_width: Normalized = Field(default=0.5, ge=0, le=1)
    jaw_width: Normalized = Field(default=0.5, ge=0, le=1)
    eye_size: Normalized = Field(default=0.5, ge=0, le=1)
    eye_distance: Normalized = Field(default=0.5, ge=0, le=1)
    nose_length: Normalized = Field(default=0.5, ge=0, le=1)
    mouth_width: Normalized = Field(default=0.5, ge=0, le=1)


class AppearanceParameters(BaseModel):
    skin_color: str = "#d7a17d"
    hair_id: str = "hair-short-001"
    hair_color: str = "#241a17"


class AvatarConfig(BaseModel):
    body: BodyParameters = Field(default_factory=BodyParameters)
    face: FaceParameters = Field(default_factory=FaceParameters)
    appearance: AppearanceParameters = Field(default_factory=AppearanceParameters)
