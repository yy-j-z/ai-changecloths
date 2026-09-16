# 3D 资产目录

```text
assets/
├─ source/       # Blender 源文件，不直接由网页加载
├─ models/       # 优化后的 GLB 人体、服装和头发
├─ animations/   # 独立或合并的动作 GLB
└─ textures/     # 必须单独保存时使用的贴图
```

不要提交来源不明的模型。每个外部素材必须登记到 `docs/asset-licenses.csv`。
大型二进制资产建议启用 Git LFS：`git lfs track "*.glb" "*.blend"`。

