# 不愿透露项目名称的项目

## Usage
### Edit [.env file](./.env)
```dotenv
# 水平风速下限
HORIZ_WIND_MIN=-3
# 水平风速上限
HORIZ_WIND_MAX=3
# 垂直风速下限
VERT_WIND_MIN=-0.1
# 垂直风速上限
VERT_WIND_MAX=0.1
# 沉降高度下限
SUBSIDE_HEIGHT_MIN=0.1
# 沉降高度上限
SUBSIDE_HEIGHT_MAX=0.5
# 沉降速度下限
SUBSIDE_SPEED_MIN=0.1
# 沉降速度上限
SUBSIDE_SPEED_MAX=0.5
# 沉降时间下限
PLANT_HEIGHT_MIN=0.1
# 沉降时间上限
PLANT_HEIGHT_MAX=0.5
```

### Run

| Argument     | Description | Default Value |
|:-------------|:------------|:--------------|
| `--width`    | 场地宽度        | `100`         |
| `--height`   | 场地长度        | `100`         |
| `--interval` | 更新间隔        | `100`         |
| `--frames`   | 总帧数         | `100`         |

```bash
python main.py --interval 100 --frames 100
```

### Interact
#### 暂停
按下 `space` 键暂停，再次按下恢复。
#### 保存帧
按下 `enter` 键保存当前帧。
#### 保存动图
按下 `a` 键保存动图。
#### 退出
按下 `esc` 键退出。
#### 重置
按下 `r` 键重置场地。
