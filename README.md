# 形镜 AI Fitting Mirror

软件工程课程项目：参数化 3D 数字人创建与虚拟试装。

用户可以调整身材和脸型、选择头发与外观，或通过正脸照片生成初始捏脸参数，然后在数字形象上试穿统一骨骼和 Morph Target 规范的三维服装。穿搭顾问智能体能够理解自然语言需求，调用商品、尺码、搭配和试穿工具，并直接更新 3D 数字人。

## 项目边界

本项目提供视觉化数字形象和尺码建议，不承诺单张照片精确恢复真人三维身体、医学级围度测量或实时布料物理仿真。详细验收范围见 [`docs/01-MVP与验收标准.md`](docs/01-MVP与验收标准.md)。

## 技术栈

| 模块              | 技术                                                          |
| ----------------- | ------------------------------------------------------------- |
| Web 与 3D         | Vue 3、TypeScript、Three.js、Pinia、Vite                      |
| 业务 API 与智能体 | Python 3.11、FastAPI、受控工具调用、SQLAlchemy、Alembic       |
| AI 服务           | FastAPI、MediaPipe、OpenCV（视觉依赖按需安装）                |
| 数据库            | MySQL 8.4                                                     |
| 3D 资产           | Blender 4.2 LTS、glTF/GLB、统一 Armature 与 Morph Targets     |
| 质量工具          | ESLint、Prettier、Ruff、Vitest、pytest、Husky、GitHub Actions |

## 目录

```text
ai-fitting-mirror/
├─ frontend/          # Vue + Three.js 数字人工作台
├─ server/            # 唯一对外的业务 API
├─ ai-service/        # 内部算法服务
├─ assets/            # Blender 源文件、GLB、动画与贴图
├─ docs/              # 需求、架构、开发与资产规范
├─ infra/             # MySQL 开发环境
├─ scripts/           # Windows 一键安装、启动和检查脚本
└─ .github/workflows/ # PR 自动质量检查
```

## 环境要求

- Git
- Node.js 22
- Python 3.11
- Docker Desktop（需要 MySQL 时）
- Blender 4.2 LTS（3D 资产成员）

不要使用系统全局 Python 安装项目依赖。项目统一使用根目录 `.venv`。

## 首次运行

```powershell
git clone <repository-url>
cd ai-fitting-mirror
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
Copy-Item server/.env.example server/.env
Copy-Item ai-service/.env.example ai-service/.env
Copy-Item frontend/.env.example frontend/.env
```

需要数据库时启动 MySQL：

```powershell
docker compose -f infra/compose.yml up -d
```

启动全部开发服务：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev.ps1
```

| 服务          | 地址                       |
| ------------- | -------------------------- |
| 数字人工作台  | http://127.0.0.1:5173      |
| 业务 API 文档 | http://127.0.0.1:8000/docs |
| AI 服务文档   | http://127.0.0.1:8001/docs |

## 提交前检查

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check.ps1
```

该命令执行前端 lint、测试和构建，以及 Python Ruff 和 pytest。GitHub PR 会执行相同检查。

## AI 视觉依赖

普通前后端成员不需要安装大型视觉依赖。负责照片分析的成员使用：

```powershell
.venv\Scripts\python -m pip install -r ai-service/requirements-ai.txt
```

## 穿搭顾问智能体

默认使用无需密钥的 demo planner，启动服务后即可演示完整工具链：

```text
用户需求 → 查询商品 → 推荐尺码 → 检查搭配 → 应用到 3D 数字人
```

接口为 `POST /api/v1/assistant/chat`。真实大模型通过 `IntentPlanner` adapter 接入，商品价格、库存和尺码仍由服务端工具提供，不能由模型编造。详细约定见 [`docs/05-穿搭顾问智能体.md`](docs/05-穿搭顾问智能体.md)。

## 3D 资产协作

首个开发目标不是批量寻找服装，而是完成一条可工作的资产链路：

1. 一个基础人体和统一 Armature。
2. 一个身体 Morph Target。
3. 一件绑定相同骨骼和 Morph Target 的上衣。
4. 导出 GLB 并在 Three.js 中完成调节、旋转和动作验证。

资产命名、导出检查和许可证要求见 [`docs/04-Blender资产规范.md`](docs/04-Blender资产规范.md)。大型 `.blend` 和 `.glb` 建议启用 Git LFS。

## 分工建议

| 角色         | 主要责任                                        |
| ------------ | ----------------------------------------------- |
| 前端/3D      | Three.js 场景、捏人控件、试装交互和截图         |
| 业务后端     | 用户、商品、数字人配置、收藏、试穿记录和后台    |
| AI           | 人脸关键点、照片参数映射、尺码与搭配推荐        |
| 3D 资产/集成 | Blender、骨骼、Morph Target、服装权重和穿模测试 |

