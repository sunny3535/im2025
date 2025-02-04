from setuptools import setup, find_packages

setup(
    name="im2025",
    version="0.1",
    packages=find_packages(),
    install_requires=['ffmpeg-python',],  # 필요한 패키지가 있다면 여기에 추가 (예: ['numpy', 'pandas'])
)
