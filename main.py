# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform
import os
from datetime import datetime

# Android权限处理
if platform == 'android':
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.RECORD_AUDIO,
                         Permission.WRITE_EXTERNAL_STORAGE,
                         Permission.READ_EXTERNAL_STORAGE])

    # 获取Android存储路径
    from android.storage import primary_external_storage_path
    from android.storage import app_storage_path

# 设置窗口大小
if platform != 'android':
    Window.size = (360, 640)


def get_system_font():
    """获取系统字体"""
    if platform == 'android':
        return 'DroidSansFallback'
    elif platform == 'win':
        return 'SimSun'
    elif platform == 'linux':
        return 'WenQuanYi Micro Hei'
    else:
        return 'Arial'


SYSTEM_FONT = get_system_font()


class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.audio_file = None
        self.start_time = None

    def get_storage_path(self):
        """获取存储路径"""
        if platform == 'android':
            try:
                # 尝试获取外部存储
                base_dir = primary_external_storage_path()
                record_dir = os.path.join(base_dir, 'Recordings')
                if not os.path.exists(record_dir):
                    os.makedirs(record_dir)
                return record_dir
            except:
                # 回退到应用存储
                return app_storage_path()
        else:
            # 桌面环境
            return os.path.expanduser('~/Recordings')

    def start_recording(self, filename):
        try:
            # 确保存储目录存在
            storage_dir = self.get_storage_path()
            if not os.path.exists(storage_dir):
                os.makedirs(storage_dir)

            full_path = os.path.join(storage_dir, filename)

            self.is_recording = True
            self.start_time = datetime.now()
            self.audio_file = full_path

            print(f"开始录音: {full_path}")
            return True
        except Exception as e:
            print(f"开始录音失败: {str(e)}")
            return False

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            duration = (datetime.now() - self.start_time).total_seconds()
            print(f"停止录音: {self.audio_file}, 时长: {duration:.2f}秒")
            return True
        return False


class RecorderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "工程录音管理"

    def build(self):
        self.recorder = AudioRecorder()
        self.recording = False

        layout = BoxLayout(
            orientation='vertical',
            padding='20dp',
            spacing='15dp'
        )
        self.create_widgets_with_font(layout)
        return layout

    def create_widgets_with_font(self, layout):
        # 标题
        title = Label(
            text='工程录音管理',
            size_hint=(1, 0.12),
            font_size='24sp',
            bold=True
        )
        title.font_name = SYSTEM_FONT
        layout.add_widget(title)

        # 项目名称
        project_label = Label(
            text='项目名称:',
            size_hint=(1, 0.06),
            font_size='16sp',
            halign='left'
        )
        project_label.font_name = SYSTEM_FONT
        layout.add_widget(project_label)

        self.project_input = TextInput(
            text='',
            hint_text='请输入项目名称',
            size_hint=(1, 0.1),
            multiline=False,
            font_size='18sp',
            padding='10dp'
        )
        self.project_input.font_name = SYSTEM_FONT
        layout.add_widget(self.project_input)

        # 构件名称
        component_label = Label(
            text='构件名称:',
            size_hint=(1, 0.06),
            font_size='16sp',
            halign='left'
        )
        component_label.font_name = SYSTEM_FONT
        layout.add_widget(component_label)

        self.component_input = TextInput(
            text='',
            hint_text='请输入构件名称',
            size_hint=(1, 0.1),
            multiline=False,
            font_size='18sp',
            padding='10dp'
        )
        self.component_input.font_name = SYSTEM_FONT
        layout.add_widget(self.component_input)

        # 文件提示
        extension_label = Label(
            text='文件将保存为: 项目_构件_时间.wav',
            size_hint=(1, 0.06),
            font_size='12sp',
            color=(0.6, 0.6, 0.6, 1)
        )
        extension_label.font_name = SYSTEM_FONT
        layout.add_widget(extension_label)

        # 录音按钮
        self.record_button = Button(
            text='开始录音',
            size_hint=(1, 0.2),
            background_color=(0.9, 0.3, 0.3, 1),
            font_size='20sp',
            bold=True
        )
        self.record_button.font_name = SYSTEM_FONT
        self.record_button.bind(on_press=self.toggle_recording)
        layout.add_widget(self.record_button)

        # 状态标签
        self.status_label = Label(
            text='准备就绪，请填写项目名称和构件名称',
            size_hint=(1, 0.12),
            font_size='16sp'
        )
        self.status_label.font_name = SYSTEM_FONT
        layout.add_widget(self.status_label)

        # 使用说明
        instruction_label = Label(
            text='使用方法:\n1. 填写项目名称和构件名称\n2. 点击按钮开始录音\n3. 再次点击停止录音',
            size_hint=(1, 0.18),
            font_size='14sp',
            color=(0.4, 0.4, 0.4, 1)
        )
        instruction_label.font_name = SYSTEM_FONT
        layout.add_widget(instruction_label)

    def generate_filename(self):
        project_name = self.project_input.text.strip() or "项目"
        component_name = self.component_input.text.strip() or "构件"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        project_name = self.clean_filename(project_name)
        component_name = self.clean_filename(component_name)

        return f"{project_name}_{component_name}_{timestamp}.wav"

    def clean_filename(self, filename):
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()[:50]

    def toggle_recording(self, instance):
        if not self.recording:
            project_name = self.project_input.text.strip()
            component_name = self.component_input.text.strip()

            if not project_name:
                self.status_label.text = "错误: 请填写项目名称"
                return
            elif not component_name:
                self.status_label.text = "错误: 请填写构件名称"
                return

            filename = self.generate_filename()

            if self.recorder.start_recording(filename):
                self.recording = True
                self.record_button.text = "停止录音"
                self.record_button.background_color = (0.3, 0.8, 0.3, 1)
                self.status_label.text = f"录音中..."
                self.project_input.disabled = True
                self.component_input.disabled = True
        else:
            if self.recorder.stop_recording():
                self.recording = False
                self.record_button.text = "开始录音"
                self.record_button.background_color = (0.9, 0.3, 0.3, 1)
                self.status_label.text = f"已保存到录音文件夹"
                self.project_input.disabled = False
                self.component_input.disabled = False


if __name__ == '__main__':
    RecorderApp().run()