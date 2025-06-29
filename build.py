#!/usr/bin/env python3
"""
Build script for Employee Face Registration and Tracking application
Creates a standalone executable using PyInstaller
Uses --onedir mode for maximum compatibility (recommended for distribution)
"""

import os
import sys
import subprocess
import shutil
import webbrowser
from pathlib import Path

def install_requirements():
    """Install all requirements from requirements.txt"""
    print("Installing requirements...")
    try:
        if not os.path.exists('requirements.txt'):
            print("✗ requirements.txt not found")
            return False
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False

def check_pyinstaller():
    """Check if PyInstaller is installed, install if not"""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False

def check_vcredist():
    # Check for Visual C++ Redistributable DLLs
    vcredist_paths = [
        r"C:\Windows\System32\vcruntime140.dll",
        r"C:\Windows\SysWOW64\vcruntime140.dll",
        r"C:\Windows\System32\msvcp140_1.dll",
        r"C:\Windows\SysWOW64\msvcp140_1.dll"
    ]
    for path in vcredist_paths:
        if os.path.exists(path):
            return True
    return False

def offer_vcredist_install():
    print("\nVisual C++ Redistributable is required for this application.")
    print("If you see a DLL error on the target PC, install it from:")
    print("https://aka.ms/vs/17/release/vc_redist.x64.exe")
    choice = input("\nDo you want to open the download page now? (y/n): ").strip().lower()
    if choice == 'y':
        webbrowser.open("https://aka.ms/vs/17/release/vc_redist.x64.exe")
        print("Please install it and re-run the application if you see a DLL error.")

def build_executable_onedir():
    """Build the executable using PyInstaller with --onedir (robust for distribution)"""
    print("Building executable with --onedir (recommended for distribution)...")
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",                     # Directory with executable and dependencies
        "--windowed",                   # No console window
        "--name=Employee_Face_Registration_Tracking",  # Executable name
        "--add-data=data.py;.",         # Include data module
        "--collect-all=cv2",            # Collect all OpenCV modules
        "--collect-all=retinaface",     # Collect all RetinaFace modules
        "--collect-all=numpy",          # Collect all NumPy modules
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.simpledialog",
        "--hidden-import=cv2",
        "--hidden-import=PIL",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
        "--hidden-import=retinaface",
        "--hidden-import=numpy",
        "--hidden-import=data",
        "--hidden-import=sqlite3",
        "face_detection.py"
    ]
    if os.path.exists('faces.db'):
        cmd.extend(["--add-data=faces.db;."])
    try:
        subprocess.check_call(cmd)
        print("✓ Executable built successfully with --onedir!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def open_output_folder():
    output_dir = os.path.join('dist', 'Employee_Face_Registration_Tracking')
    if os.path.exists(output_dir):
        print(f"Opening output folder: {output_dir}")
        if sys.platform == "win32":
            os.startfile(output_dir)
        else:
            subprocess.Popen(["xdg-open", output_dir])
    else:
        print("Output folder not found.")

def offer_run_exe():
    exe_path = os.path.join('dist', 'Employee_Face_Registration_Tracking', 'Employee_Face_Registration_Tracking.exe')
    if os.path.exists(exe_path):
        choice = input("\nDo you want to run the application now? (y/n): ").strip().lower()
        if choice == 'y':
            subprocess.Popen([exe_path], shell=True)
    else:
        print("Executable not found for running.")

def main():
    print("Employee Face Registration & Tracking - Build Script")
    print("=" * 50)
    if sys.platform != "win32":
        print("✗ This build script is designed for Windows only")
        return False
    if not install_requirements():
        return False
    if not check_pyinstaller():
        return False
    if not build_executable_onedir():
        return False
    print("\n" + "=" * 50)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\nFiles created:")
    print("- dist/Employee_Face_Registration_Tracking/ (Directory with executable and dependencies)")
    print("\nTo run on any Windows PC:")
    print("- Copy the entire 'dist/Employee_Face_Registration_Tracking' folder to the target PC")
    print("- Run 'Employee_Face_Registration_Tracking.exe' from inside that folder")
    if not check_vcredist():
        offer_vcredist_install()
    open_output_folder()
    offer_run_exe()
    print("\nIf you see a DLL error, install the Visual C++ Redistributable from:")
    print("https://aka.ms/vs/17/release/vc_redist.x64.exe")
    print("\nGitHub Repository:")
    print("https://github.com/needyamin/employee-face-registration-and-tracking")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nBuild failed. Please check the error messages above.")
        sys.exit(1) 