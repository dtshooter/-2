[app]
title = 工程录音管理
package.name = recorderapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 0.1
requirements = python3,kivy,jnius,android
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[android]
api = 33
minapi = 21
android.allow_backup = true
android.permissions = RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[android:meta-data]
android.app.uses_audio_input = true