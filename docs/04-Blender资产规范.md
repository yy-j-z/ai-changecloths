# Blender 与 GLB 资产规范

## 统一标准

- Blender 版本：4.2 LTS。
- 单位：Metric，1 Blender Unit = 1 metre。
- 坐标：Z 向上；导出 glTF 时使用默认坐标转换。
- 基础姿势：统一 A Pose，不混用 T Pose。
- 人体、服装共用同一套 Armature 和骨骼命名。
- 发布格式：`.glb`；`.blend` 保留为源文件。
- 模型应用 Rotation 和 Scale 后再导出。

## 命名

```text
CHR_Avatar_Base
ARM_Avatar
GAR_Tshirt_001
GAR_Jeans_001
HAIR_Short_001
MAT_Tshirt_White
MORPH_Body_Weight
MORPH_Body_Waist
MORPH_Face_JawWidth
```

人体与衣服共用的 Morph Target 名称必须完全一致。首批统一使用：

- `Body_Weight`
- `Body_Shoulder`
- `Body_Chest`
- `Body_Waist`
- `Body_Hip`
- `Body_LegLength`

## 导出前检查

1. 网格没有未应用的缩放和旋转。
2. 人体与服装使用相同 Armature。
3. 权重归一化，动作下没有明显穿模。
4. 贴图使用相对路径并打包到 GLB。
5. 单个服装 GLB 尽量小于 10 MB，贴图优先使用 1K 或 2K。
6. 在 Three.js 测试页验证骨骼、Morph Target、材质和动画。
7. 在 `asset-licenses.csv` 登记来源及许可证。

