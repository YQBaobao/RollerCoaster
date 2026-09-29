from winrt.windows.ui import shell
from winrt.windows.foundation import Size

# 创建任务栏按钮（Thumbnail Toolbar）
thumbnail_manager = shell.TaskbarManager.get_default()
if thumbnail_manager.is_supported:
    button = shell.ThumbnailToolbarButton()
    button.icon = shell.IconSource(uri="C:\\path\\to\\icon.ico")
    button.tooltip = "Click me!"
    thumbnail_manager.add_button(button)
else:
    print("Thumbnail toolbar not supported")