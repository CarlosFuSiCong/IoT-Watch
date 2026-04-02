# IoT Watch — Implementation Tasks

> 细粒度任务，便于边做边学。每个阶段含学习要点、子任务、验收标准、常见坑点。

---

## Phase 1–2: 环境与 MQTT 基础

### 学习要点

- **MQTT Broker**：设备与后端之间的「消息中转站」。设备发布消息到 Broker，后端订阅后接收。
- **Topic**：数据路由的「频道」。例如 `devices/warehouse-01/telemetry` 表示 warehouse-01 的遥测数据。
- **通配符**：`+` 匹配单层，`#` 匹配多层。`devices/+/telemetry` 可收到所有设备的遥测。

### 子任务

| 序号 | 子任务 | 说明 | 验收 | 状态 |
|------|--------|------|------|------|
| 1.1 | 安装 Docker | 本机可运行容器 | `docker --version` 正常 | ✅ |
| 1.2 | 创建 docker/docker-compose.yml | 定义 mqtt、db 服务，Docker 文件统一放 `docker/`，项目名 iotwatch | `docker compose -f docker/docker-compose.yml up` 能启动 | ✅ |
| 1.3 | 配置 Mosquitto | MQTT Broker，1883 端口 | 可连接 | ✅ |
| 1.4 | 配置 PostgreSQL | 持久化数据 | 可 psql 连接 | ✅ |
| 1.5 | 创建项目目录 | backend/、frontend/、simulator/、docker/、docs/ | 结构清晰，docker 相关统一在 docker/ | ✅ |
| 2.1 | 理解 Topic | `devices/+/telemetry` 含义 | 能解释 | ✅ |
| 2.2 | mosquitto_pub/sub 手动测试 | 发布与订阅一条消息 | 能收发 | ✅ |
| 2.3 | Python paho-mqtt 最小脚本 | 发布一条 JSON | mosquitto_sub 能收到 | ✅ |

### 常见坑点

- **MQTT 连不上**：检查 Docker 网络，确保 backend/simulator 与 mqtt 在同一网络或可访问 mqtt 的 host。
- **端口占用**：1883 若被占用，可在 compose 中映射其他端口。

---

## Phase 3: 设备模拟器

### 学习要点

- 真实设备会按固定间隔上报；模拟器让你本地测试而无需实体硬件。
- 遥测数据需符合 spec 格式，便于后端解析。

### 子任务

| 序号 | 子任务 | 说明 | 验收 | 状态 |
|------|--------|------|------|------|
| 3.1 | 定义遥测格式 | device_id, temperature, humidity, battery, timestamp (ISO8601) | 与 spec 一致 | ✅ |
| 3.2 | 单设备循环发布 | 每 2–5 秒发布 | 持续向 Broker 发送 | ✅ |
| 3.3 | 多设备（≥3） | warehouse-01、02、03 | 三条 Topic 均有数据 | ✅ |
| 3.4 | 随机波动 | 温度 25–35，电量随时间递减 | 数据有变化 | ✅ |

### 常见坑点

- **时区**：`timestamp` 建议用 UTC 或 ISO8601，后端统一解析。

---

## Phase 4–5: 后端核心与 MQTT 订阅

### 学习要点

- **Device**：设备元信息（id, name, last_seen, status）
- **SensorData**：时序遥测（每条消息一条记录）
- **Alert**：告警事件
- 后端作为「订阅者」**被动接收**数据，与 HTTP 请求不同。

### 子任务

| 序号 | 子任务 | 说明 | 验收 | 状态 |
|------|--------|------|------|------|
| 4.1 | FastAPI 骨架 | main.py、/docs、/health | Swagger 可访问 | ✅ |
| 4.2 | Device 模型 | id, name, last_seen, status, created_at | 迁移成功 | ✅ |
| 4.3 | SensorData 模型 | device_id, temperature, humidity, battery, timestamp | 外键关联 Device | ✅ |
| 4.4 | Alert 模型 | device_id, type, message, timestamp | type 枚举 | ✅ |
| 4.5 | 数据库迁移 | Alembic 或 SQLAlchemy migrate | 可重复执行 | ✅ |
| 5.1 | MQTT 订阅 | 订阅 `devices/+/telemetry` | 能收消息 | ✅ |
| 5.2 | 解析 JSON | 校验 device_id、temperature 等 | 非法格式跳过并打日志 | ✅ |
| 5.3 | 自动注册设备 | 新 device_id → 创建 Device | 首次上报即入库 | ✅ |
| 5.4 | 写入 SensorData | 每条消息一条记录 | 表中数据增长 | ✅ |
| 5.5 | 更新 last_seen | 每次收到数据更新 Device | 可判断在线 | ✅ |
| 5.6 | 启动时订阅 | FastAPI lifespan 中启动 MQTT | 后端启动即接收 | ✅ |

### 常见坑点

- **MQTT 在 FastAPI 中**：使用 `lifespan` 在应用启动时连接 MQTT，关闭时断开。
- **线程安全**：MQTT 回调与 FastAPI 可能在不同线程，注意 DB session 使用方式。

---

## Phase 6–7: 状态与告警

### 学习要点

- **心跳与超时**：物联网常用「无心跳即离线」；超时 10 秒即认为设备掉线。
- **告警规则**：从「有数据」到「有问题时提醒」是 IoT 的核心价值。

### 子任务

| 序号 | 子任务 | 说明 | 验收 | 状态 |
|------|--------|------|------|------|
| 6.1 | 理解 10 秒规则 | last_seen 超过 10s → offline | 能写出判断逻辑 | ✅ |
| 6.2 | 实现离线检测 | 每次入库时检查或定时任务 | 停模拟器后 10s 内变 offline | ✅ |
| 6.3 | 恢复 online | 收到数据时 status=online | 设备恢复即变回 | ✅ |
| 7.1 | 告警类型枚举 | HIGH_TEMPERATURE, LOW_BATTERY, OFFLINE | 与 spec 一致 | ✅ |
| 7.2 | 高温告警 | temperature > 35 → 创建 Alert | 调高温度可触发 | ✅ |
| 7.3 | 低电量告警 | battery < 20 → 创建 Alert | 调低 battery 可触发 | ✅ |
| 7.4 | 离线告警 | online→offline 时创建 | 停设备 10s 可触发 | ✅ |
| 7.5 | 防重复（可选） | 同设备同类型 5 分钟内不重复 | 避免刷屏 | ✅ |

### 常见坑点

- **离线检测时机**：可在处理每条消息时批量检查所有设备，或使用定时任务每 5s 扫描。

---

## Phase 8–10: API 与 Dashboard

### 子任务

| Phase | 子任务 | 说明 | 验收 | 状态 |
|-------|--------|------|------|------|
| 8 | GET /devices | 所有设备及 status、last_seen | 符合 api-spec | ✅ |
| 8 | GET /devices/{id} | 单设备详情 | 404 正确 | ✅ |
| 8 | GET /devices/{id}/telemetry | 分页 page、limit | 能分页 | ✅ |
| 8 | GET /alerts | 过滤 device_id、type | 可筛选 | ✅ |
| 8 | 统一响应格式 | { success, data } 或 { success, errors } | 便于前端 | ✅ |
| 9 | Vite + React 项目 | TypeScript template | `npm run dev` 可启动 | ✅ |
| 9 | API 代理配置 | vite.config proxy → localhost:8000 | 能调通接口 | ✅ |
| 9 | TanStack Query、React Router | 依赖安装 | 依赖就绪 | ✅ |
| 9 | Devices / Alerts 页 | 基础列表页 + 路由 | 数据能拉取 | ✅ |
| 10 | 总览页 | 设备数、在线数、离线数、告警数 | 数字正确 | ✅ |
| 10 | 设备列表 | 表格：Device, Status, Temp, Battery | 可点击详情 | ✅ |
| 10 | 设备详情 | 最新温度、湿度、电量 | 来自 telemetry | ✅ |
| 10 | 温度折线图 | Chart.js 或 Recharts | 能看出趋势 | ✅ |
| 10 | 告警面板 | 类型、设备、时间 | 列表可展示 | ✅ |

---

## Phase 11: 联调与验收

| 序号 | 子任务 | 说明 | 验收 | 状态 |
|------|--------|------|------|------|
| 11.1 | 一键启动 | `docker compose -f docker/docker-compose.yml up` 启动 mqtt/db；另起 simulator、frontend | 全部正常 | ✅ |
| 11.2 | 端到端数据流 | 模拟器 → MQTT → 后端 → API → 前端 | 数据完整链路 | ⬜ |
| 11.3 | 离线检测 | 停一设备，10s 内显示 offline | 符合 spec | ⬜ |
| 11.4 | 告警触发 | 高温、低电量、离线都能触发 | 三种告警可验证 | ⬜ |

---

## Phase 12: 可选增强

| 序号 | 子任务 | 说明 | 状态 |
|------|--------|------|------|
| 12.1 | WebSocket 推送 | 后端收到 MQTT → 推送给前端，实现真正实时 | ⬜ |
| 12.2 | 设备 CRUD | 增删改设备（管理员功能） | ⬜ |
| 12.3 | 异常检测 | 如连续 3 次温度骤升则告警 | ⬜ |
| 12.4 | Docker 完整化 | frontend、simulator 进 `docker/docker-compose.yml`，README 一键启动 | ⬜ |

---

**图例**：✅ 已完成　⬜ 未完成

---

**进度汇总**（截至 Phase 3 完成）

| Phase | 已完成 | 总数 |
|-------|--------|------|
| 1–2 环境与 MQTT | 8 | 8 |
| 3 设备模拟器 | 4 | 4 |
| 4–5 后端核心 | 11 | 11 |
| 6–7 状态与告警 | 8 | 8 |
| 8–10 API 与 Dashboard | 1 | 14 |
| 11 联调验收 | 1 | 4 |
| 12 可选增强 | 0 | 4 |
