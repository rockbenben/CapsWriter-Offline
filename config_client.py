import os
from collections.abc import Iterable
from pathlib import Path

# 版本信息
__version__ = '2.6'

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# 客户端配置
class ClientConfig:
    addr = '127.0.0.1'          # Server 地址
    port = '6016'               # Server 端口

    # 快捷键配置列表
    shortcuts = [
        {
            'key': 'alt_gr',        # 监听右 Alt 键（pynput 里右 Alt 的名字是 alt_gr，不是 alt_r），当作录音键
            'type': 'keyboard',     # 是键盘快捷键
            'suppress': True,        # 阻塞：右 Alt 被完全吞掉，不再触发系统 Alt 热键/AltGr（专职录音键）
            'hold_mode': False,      # 单击模式：点一下开始录音，再点一下停止（即"短按"用法）
            'threshold': 0.5,       # 单击容错：按下后须在 threshold×0.8（=0.4s）内松开，这一下才算"点击"；按更久会被当成长按——开始那下会取消录音、停止那下会失效。只作用于本键，不影响下面的 Config.threshold
            'enabled': True         # 启用此快捷键
        },
        {
            'key': 'caps_lock',     # 监听大写锁定键
            'type': 'keyboard',     # 是键盘快捷键
            'suppress': True,      # 阻塞按键（短按会补发）
            'hold_mode': True,      # 长按模式
            'enabled': False        # 已禁用
        },
        {
            'key': 'x2',
            'type': 'mouse',
            'suppress': True,
            'hold_mode': True,
            'enabled': False
        },
    ]

    threshold    = 0.3          # 快捷键触发阈值（秒）

    paste        = True         # 是否以写入剪切板然后模拟 Ctrl-V 粘贴的方式输出结果
    restore_clip = False        # 模拟粘贴后是否恢复剪贴板（关闭：恢复过快会与目标程序读剪贴板抢跑，导致粘不上）
    paste_apps   = ['WeiXin.exe', 'Telegram.exe']  # 匹配时强制粘贴

    enter_apps   = [('happ.exe', 0.5), ('hexin.exe', 0.5)]  # (应用名, 延迟秒数) 输出完成后自动回车，如同花顺，输入股票名后，需要回车才能切换

    mute_while_recording = True  # 录音时静音系统输出，录完恢复（需 pycaw；系统本就静音时不碰）

    save_audio = True           # 是否保存录音文件
    audio_name_len = 20         # 将录音识别结果的前多少个字存储到录音文件名中，建议不要超过200

    show_recording_toast = True  # 录音时是否在屏幕上显示悬浮状态提示（深色胶囊+声波条），松开按键后转为「正在转文字」，文字开始输出时消失
    recording_toast_margin = 16  # 悬浮胶囊底边距任务栏的像素间距，越小越贴近任务栏
    recording_toast_opacity = 0.88  # 悬浮胶囊整体不透明度（0.2~1.0），越小越透，背景透出越多
    recording_toast_sensitivity = 12.0  # 波形对麦克风音量的灵敏度，说话时波形不够跳就调大、太满就调小
    recording_toast_noise_gate = 0.010  # 噪声门：麦克风音量低于此值视为静音，没说话也在动就调大（如 0.02）
    
    context = ''                # 提示词上下文，用于辅助 Fun-ASR-Nano 模型识别（例如输入人名、地名、专业术语等）
    language = 'auto'           # 识别语言：'auto', 'chinese', 'english', 'japanese' 等（各引擎支持范围不同）

    trash_punc = '，。,.'       # 识别结果要消除的末尾标点
    trash_punc_thresh = 8       # 识别结果的单词数量低于阈值时，强制去除末尾标点
    trash_punc_apps = ['WeiXin.exe', ]   # 对于指定的应用，强制去除末尾标点

    traditional_convert = False     # 是否将识别结果转换为繁体中文
    traditional_locale = 'zh-hant'  # 繁体地区：'zh-hant'（标准繁体）, 'zh-tw'（台湾繁体）, 'zh-hk'（香港繁体）

    hot = True                 # 是否启用热词替换（统一 RAG 匹配）
    hot_thresh = 0.85           # RAG 替换热词阈值（高阈值，用于实际替换）
    hot_similar = 0.6           # RAG 相似热词阈值（低阈值，用于 LLM 上下文）
    hot_rule = True             # 是否启用自定义规则替换（基于正则表达式）

    llm_enabled = True          # 是否启用 LLM 润色功能，需要配置 LLM/ 目录下的角色文件
    llm_stop_key = 'esc'        # 中断 LLM 输出的快捷键

    enable_tray = True          # 客户端默认启用托盘图标功能

    # 日志配置
    log_level = 'DEBUG'          # 日志级别：'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'

    mic_seg_duration = 60       # 麦克风听写时分段长度：60秒
    mic_seg_overlap = 4         # 麦克风听写时分段重叠：4秒

    file_seg_duration = 60      # 转录文件时分段长度
    file_seg_overlap = 4        # 转录文件时分段重叠

    file_save_srt = True        # 转录文件时是否保存 srt 字幕
    file_save_txt = True        # 转录文件时是否保存 txt 文本（按标点切分后的）
    file_save_json = True       # 转录文件时是否保存 json 结果（含原始时间戳）
    file_save_merge = False      # 转录文件时是否保存 merge.txt（未切分的段落长文本）

    udp_broadcast = False               # 是否启用 UDP 广播输出结果
    udp_broadcast_targets = [           # UDP 广播目标地址列表，格式: (地址, 端口)
        ('127.255.255.255', 6017),      # 本地回环广播
        # ('192.168.1.255', 6017),      # 局域网广播（示例，按需启用）
    ]

    udp_control = False             # 是否启用 UDP 控制录音（外部程序发送 START/STOP 命令）
    udp_control_addr = '127.0.0.1'  # UDP 控制监听地址（'0.0.0.0' 允许外部访问）
    udp_control_port = 6018         # UDP 控制监听端口


# 快捷键配置说明
r"""
快捷键配置字段说明：
  key        - 按键名称（见下方可用按键列表）
  type       - 输入类型：'keyboard'（键盘）或 'mouse'（鼠标）
  suppress   - 是否阻塞按键（True=阻塞，False=不阻塞）
  hold_mode  - 长按模式（True=按下录音松开停止，False=单击开始再次单击停止）
  enabled    - 是否启用此快捷键

阻塞模式说明：
  - 阻塞模式  ：长按录音识别，短按（<0.3秒）则自动补发按键，不影响单击功能
  - 非阻塞模式：对于 CapsLock/NumLock/ScrollLock 这类切换键，松开时会自动补发，以恢复按键状态

可用按键名称：

  字母数字：a - z, 0 - 9（大键盘）

  符号键：, . / \ ` ' - = [ ] ; '


  功能键：f1 - f24

  控制键:
      ctrl_l,   ctrl_r,
      shift,  shift_r,
      alt_l,    alt_gr,
      cmd,    cmd_r

  特殊键：
      space, enter, tab, backspace, delete, insert, home, end
      page_up, page_down, esc, caps_lock, num_lock, scroll_lock
      print_screen, pause, menu

  方向键：up, down, left, right

  鼠标键：x1, x2

示例配置：
  {'key': 'caps_lock', 'type': 'keyboard', 'suppress': False, 'hold_mode': True, 'enabled': True}, 
  {'key': 'f12', 'type': 'keyboard', 'suppress': True, 'hold_mode': True, 'enabled': True}, 
  {'key': 'x2', 'type': 'mouse', 'suppress': True, 'hold_mode': True, 'enabled': True}, 
"""

