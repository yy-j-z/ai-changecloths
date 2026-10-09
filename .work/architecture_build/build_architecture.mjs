import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = "C:\\课程\\软件工程-大三上\\ai换装";
const buildDir = path.join(workspaceDir, ".work", "architecture_build");
const outputDir = path.join(workspaceDir, "deliverables");
const skillDir = "C:\\Users\\jyy\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.909.12148\\skills\\presentations";
const pythonExecutable = "C:\\Users\\jyy\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe";
const finalPath = path.join(outputDir, "形镜AI变装_架构图_可编辑.pptx");
const fontFamily = "Microsoft YaHei";

await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });

const presentation = Presentation.create({ slideSize: { width: 1600, height: 1000 } });

const C = {
  ink: "#243447",
  muted: "#60758B",
  blue: "#DCEAF7",
  blueStrong: "#4B79C6",
  green: "#DFF1DC",
  greenStrong: "#5A9A63",
  orange: "#FCE8D4",
  orangeStrong: "#D98945",
  cyan: "#DDF3F2",
  cyanStrong: "#3D9897",
  purple: "#ECE2F3",
  purpleStrong: "#8B69A6",
  yellow: "#FFF1C9",
  yellowStrong: "#B88A2D",
  gray: "#F5F7F9",
  line: "#75879A",
  white: "#FFFFFF",
};

function addText(slide, text, x, y, w, h, opts = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    typeface: fontFamily,
    fontSize: opts.fontSize ?? 20,
    bold: opts.bold ?? false,
    color: opts.color ?? C.ink,
    alignment: opts.alignment ?? "center",
    verticalAlignment: opts.verticalAlignment ?? "middle",
    autoFit: "shrinkText",
    wrap: "square",
    insets: opts.insets ?? { top: 4, right: 6, bottom: 4, left: 6 },
  };
  return shape;
}

function addBox(slide, text, x, y, w, h, opts = {}) {
  const shape = slide.shapes.add({
    geometry: opts.geometry ?? "roundRect",
    position: { left: x, top: y, width: w, height: h },
    fill: opts.fill ?? C.white,
    line: {
      style: opts.lineStyle ?? "solid",
      fill: opts.stroke ?? C.line,
      width: opts.lineWidth ?? 1.5,
    },
    shadow: opts.shadow ?? "shadow-none",
  });
  shape.text = text;
  shape.text.style = {
    typeface: fontFamily,
    fontSize: opts.fontSize ?? 18,
    bold: opts.bold ?? false,
    color: opts.color ?? C.ink,
    alignment: opts.alignment ?? "center",
    verticalAlignment: "middle",
    autoFit: "shrinkText",
    wrap: "square",
    insets: { top: 5, right: 8, bottom: 5, left: 8 },
  };
  return shape;
}

function addBand(slide, label, y, h, palette, items, columns, note = "") {
  slide.shapes.add({
    geometry: "roundRect",
    position: { left: 54, top: y, width: 1492, height: h },
    fill: "#FFFFFF",
    line: { style: "dashed", fill: palette.strong, width: 1.6 },
  });
  addBox(slide, label, 70, y + 12, 150, h - 24, {
    fill: palette.fill,
    stroke: palette.strong,
    fontSize: 21,
    bold: true,
  });
  const x0 = 246;
  const usable = 1278;
  const gap = 12;
  const colW = (usable - gap * (columns - 1)) / columns;
  const rows = Math.ceil(items.length / columns);
  const rowGap = 10;
  const topPad = note ? 34 : 15;
  const bottomPad = 14;
  const rowH = (h - topPad - bottomPad - rowGap * (rows - 1)) / rows;
  items.forEach((item, idx) => {
    const col = idx % columns;
    const row = Math.floor(idx / columns);
    addBox(slide, item, x0 + col * (colW + gap), y + topPad + row * (rowH + rowGap), colW, rowH, {
      fill: palette.fill,
      stroke: palette.strong,
      fontSize: 17,
      bold: item.includes("/api/v1") || item.includes("IntentPlanner"),
    });
  });
  if (note) addText(slide, note, x0, y + 3, usable, 28, { fontSize: 14, color: C.muted, alignment: "left" });
}

function addDownArrow(slide, y1, y2) {
  const a = slide.shapes.add({
    geometry: "downArrow",
    position: { left: 138, top: y1, width: 26, height: Math.max(18, y2 - y1) },
    fill: C.blueStrong,
    line: { fill: C.blueStrong, width: 0 },
  });
  return a;
}

function addConnector(slide, from, to, opts = {}) {
  return slide.shapes.connect(from, to, {
    kind: opts.kind ?? "elbow",
    fromSide: opts.fromSide,
    toSide: opts.toSide,
    line: { style: opts.style ?? "solid", fill: opts.color ?? C.blueStrong, width: opts.width ?? 3 },
    head: opts.head === false ? { type: "none" } : { type: "triangle", width: "med", length: "med" },
    tail: opts.tail ? { type: "triangle", width: "med", length: "med" } : { type: "none" },
  });
}

// 图 1：系统功能架构图
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addText(slide, "形镜 AI 变装系统功能架构", 55, 28, 1490, 48, { fontSize: 30, bold: true, alignment: "left" });
  addText(slide, "浏览器只访问业务 API；智能体通过白名单工具驱动推荐和 3D 换装", 55, 78, 1490, 34, { fontSize: 16, color: C.muted, alignment: "left" });

  const bands = [
    { y: 125, h: 100, label: "接入层", p: { fill: C.blue, strong: C.blueStrong }, items: ["用户 Web 端", "3D 数字人工作台", "穿搭顾问对话", "商家管理后台（可选）"], c: 4 },
    { y: 237, h: 90, label: "接口层", p: { fill: C.green, strong: C.greenStrong }, items: ["统一业务入口  /api/v1", "认证与参数校验", "统一响应与错误处理"], c: 3, note: "Vite 开发代理将 /api 请求转发到业务服务" },
    { y: 339, h: 144, label: "业务服务层", p: { fill: C.orange, strong: C.orangeStrong }, items: ["用户与账号", "数字人档案", "商品与 SKU", "虚拟试装", "收藏与试穿记录", "资产与后台管理"], c: 3 },
    { y: 495, h: 166, label: "智能体层", p: { fill: C.yellow, strong: C.yellowStrong }, items: ["IntentPlanner\ndemo / LLM adapter", "search_products\n商品检索", "recommend_size\n尺码推荐", "check_outfit_compatibility\n搭配校验", "apply_outfit\n应用换装", "tool_events + outfit_action\n可审计输出"], c: 3, note: "大模型只负责理解需求与选择工具，不能直接修改数据库或编造商品信息" },
    { y: 673, h: 116, label: "算法服务层", p: { fill: C.cyan, strong: C.cyanStrong }, items: ["人脸关键点检测", "照片参数估计", "身材与脸型参数映射", "尺码推荐算法"], c: 4, note: "内部算法接口 /internal/v1；算法服务不保存业务数据" },
    { y: 801, h: 142, label: "数据与资产层", p: { fill: C.purple, strong: C.purpleStrong }, items: ["MySQL 8.4\n用户、商品、记录", "向量库（规划）\n商品语义检索", "对象存储 / 本地文件\n照片、截图、贴图", "Blender 4.2 → GLB\n骨骼、Morph、服装"], c: 4 },
  ];
  bands.forEach((b) => addBand(slide, b.label, b.y, b.h, b.p, b.items, b.c, b.note ?? ""));
  for (let i = 0; i < bands.length - 1; i++) addDownArrow(slide, bands[i].y + bands[i].h - 2, bands[i + 1].y + 3);
  addText(slide, "请求与业务动作向下编排，结构化结果返回前端并更新 Three.js 数字人", 380, 950, 1140, 30, { fontSize: 14, color: C.muted, alignment: "right" });
}

// 图 2：系统总体技术架构图
{
  const slide = presentation.slides.add();
  slide.background.fill = C.white;
  addText(slide, "形镜 AI 变装系统总体技术架构", 55, 28, 1490, 48, { fontSize: 30, bold: true, alignment: "left" });

  slide.shapes.add({
    geometry: "roundRect",
    position: { left: 520, top: 112, width: 1040, height: 790 },
    fill: "#FBFCFD",
    line: { style: "dashed", fill: C.line, width: 1.6 },
  });
  addText(slide, "开发机 / 课程答辩环境", 545, 118, 400, 30, { fontSize: 16, bold: true, color: C.muted, alignment: "left" });

  const client = addBox(slide, "浏览器客户端\n\nVue 3 + TypeScript\nThree.js + Pinia + Vite\n\n开发端口 5173", 65, 170, 380, 245, { fill: C.blue, stroke: C.blueStrong, fontSize: 21, bold: true, lineWidth: 2 });
  const server = addBox(slide, "业务服务 server\n\nFastAPI  /api/v1\n认证、业务规则、持久化\n智能体编排与工具白名单\n\n端口 8000", 590, 165, 430, 270, { fill: C.orange, stroke: C.orangeStrong, fontSize: 21, bold: true, lineWidth: 2 });
  const ai = addBox(slide, "算法服务 ai-service\n\nFastAPI  /internal/v1\n关键点与参数估计\n尺码推荐算法\n\n端口 8001", 1120, 170, 380, 245, { fill: C.cyan, stroke: C.cyanStrong, fontSize: 21, bold: true, lineWidth: 2 });
  const assets = addBox(slide, "3D 资产制作与发布\n\nBlender 4.2 LTS\n统一 Armature / Morph Target\n导出 glTF / GLB\n离线制作，不作为运行时服务", 65, 570, 380, 235, { fill: C.yellow, stroke: C.yellowStrong, fontSize: 20, bold: true, lineWidth: 2 });
  const data = addBox(slide, "数据与文件\n\nMySQL 8.4（Docker Compose）  3306\n用户、商品、数字人、试穿记录\n\n本地文件 / 对象存储\nGLB、贴图、上传照片与截图", 590, 545, 430, 285, { fill: C.purple, stroke: C.purpleStrong, fontSize: 20, bold: true, lineWidth: 2 });
  const llm = addBox(slide, "可替换大模型服务（可选）\n\n兼容 Chat Completions 协议\n只返回结构化意图\n商品、库存与尺码仍由服务端工具提供\n默认 demo planner 无需外部网络", 1120, 560, 380, 255, { fill: C.green, stroke: C.greenStrong, fontSize: 19, bold: true, lineWidth: 2 });

  addConnector(slide, client, server, { fromSide: "right", toSide: "left", color: C.blueStrong, tail: true, kind: "straight" });
  addText(slide, "HTTP  /api/v1\nVite 开发代理", 452, 205, 132, 54, { fontSize: 14, bold: true, color: C.blueStrong });

  addConnector(slide, server, ai, { fromSide: "right", toSide: "left", color: C.cyanStrong, tail: true, kind: "straight" });
  addText(slide, "内部 HTTP\n/internal/v1", 1018, 205, 102, 54, { fontSize: 12, bold: true, color: C.cyanStrong });

  addConnector(slide, server, data, { fromSide: "bottom", toSide: "top", color: C.purpleStrong, tail: true, kind: "straight" });
  addText(slide, "SQLAlchemy / 文件访问", 590, 470, 190, 36, { fontSize: 14, bold: true, color: C.purpleStrong, alignment: "right" });

  addConnector(slide, server, llm, { fromSide: "bottom", toSide: "top", color: C.greenStrong, tail: true, kind: "elbow" });
  addText(slide, "HTTPS（compatible 模式）", 1125, 455, 280, 36, { fontSize: 14, bold: true, color: C.greenStrong });

  addConnector(slide, assets, data, { fromSide: "right", toSide: "left", color: C.yellowStrong, kind: "straight" });
  addText(slide, "发布 GLB 与贴图", 448, 600, 132, 36, { fontSize: 14, bold: true, color: C.yellowStrong });
  addText(slide, "Three.js 通过业务服务返回的资产地址加载 GLB 与贴图", 65, 445, 455, 72, { fontSize: 15, bold: true, color: C.purpleStrong });

  addText(slide, "约束：浏览器不直接访问算法服务；ai-service 不访问业务数据库", 55, 916, 1490, 40, { fontSize: 17, bold: true, color: C.ink, alignment: "center" });
}

const stagingDir = path.join(buildDir, "finalizer");
await fs.mkdir(stagingDir, { recursive: true });
const candidatePath = path.join(stagingDir, "architecture-candidate.pptx");
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);

await fs.copyFile(candidatePath, finalPath);

console.log(finalPath);
