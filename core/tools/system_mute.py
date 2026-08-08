# coding: utf-8
"""
录音时静音系统输出

按下录音键时静音系统主音量，录音结束后恢复。
用 SetMute 读写静音位（而非模拟静音键的 toggle），系统本来就静音时不碰、也不恢复。
"""

import atexit

from core.logger import get_logger

logger = get_logger('client')

try:
    import comtypes
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    _available = True
except ImportError:
    _available = False
    logger.warning("pycaw 未安装，录音静音功能不可用（pip install pycaw）")

# 我们是否执行了静音（系统本来就静音则保持 False，不恢复）
_muted_by_us = False


def _endpoint():
    """获取默认输出设备的音量接口（每次现取，兼容不同调用线程与设备切换）"""
    comtypes.CoInitialize()
    device = AudioUtilities.GetSpeakers()
    if hasattr(device, 'EndpointVolume'):  # 新版 pycaw 返回 AudioDevice 包装
        return device.EndpointVolume
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)  # 旧版返回裸 IMMDevice
    return cast(interface, POINTER(IAudioEndpointVolume))


def mute() -> None:
    """录音开始：静音系统输出（幂等）"""
    global _muted_by_us
    if not _available or _muted_by_us:
        return
    try:
        volume = _endpoint()
        if not volume.GetMute():
            volume.SetMute(1, None)
            _muted_by_us = True
    except Exception as e:
        logger.warning(f"静音系统输出失败: {e}")


def unmute() -> None:
    """录音结束：仅恢复我们自己静音的那次（幂等）"""
    global _muted_by_us
    if not _muted_by_us:
        return
    try:
        _endpoint().SetMute(0, None)
    except Exception as e:
        logger.warning(f"恢复系统输出失败: {e}")
    finally:
        _muted_by_us = False


atexit.register(unmute)  # 兜底：进程退出时不留哑巴
