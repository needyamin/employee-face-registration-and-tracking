#!/usr/bin/env python3
"""
Build script for Employee Face Registration and Tracking application
Creates a standalone executable using PyInstaller
Supports both portable and installer modes with Inno Setup
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def get_user_choice():
    """Get user choice for build type"""
    print("Employee Face Registration & Tracking - Build Options")
    print("=" * 50)
    print("1. Portable Executable (standalone .exe file)")
    print("2. Installer (creates both .exe and installer)")
    print("=" * 50)
    
    while True:
        try:
            choice = input("Select build type (1 or 2): ").strip()
            if choice == "1":
                return "portable"
            elif choice == "2":
                return "installer"
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nBuild cancelled.")
            sys.exit(0)

def install_requirements():
    """Install all requirements from requirements.txt"""
    print("Installing requirements...")
    try:
        # Check if requirements.txt exists
        if not os.path.exists('requirements.txt'):
            print("✗ requirements.txt not found")
            return False
        
        # Install requirements
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

def check_inno_setup():
    """Check if Inno Setup is installed"""
    # Check common Inno Setup installation paths
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe"
    ]
    
    for path in inno_paths:
        if os.path.exists(path):
            print(f"✓ Inno Setup found at: {path}")
            return path
    
    print("✗ Inno Setup not found. Please install Inno Setup 6 from:")
    print("  https://jrsoftware.org/isinfo.php")
    print("  Or use portable mode instead.")
    return None

def create_spec_file():
    """Create a PyInstaller spec file for the application"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['face_detection.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data.py', '.'),
        ('faces.db', '.') if os.path.exists('faces.db') else None,
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'cv2',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'retinaface',
        'numpy',
        'os',
        'datetime',
        'threading',
        'queue',
        'data',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Employee_Face_Registration_Tracking',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    # Clean up None entries from datas
    spec_content = spec_content.replace("('faces.db', '.') if os.path.exists('faces.db') else None,", "")
    
    with open('face_detection.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✓ PyInstaller spec file created")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=Employee_Face_Registration_Tracking",  # Executable name
        "--add-data=data.py;.",         # Include data module
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
    
    # Add database file if exists
    if os.path.exists('faces.db'):
        cmd.extend(["--add-data=faces.db;."])
    
    try:
        subprocess.check_call(cmd)
        print("✓ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def create_inno_setup_script():
    """Create Inno Setup script for installer"""
    # Check if LICENSE file exists
    license_line = "LicenseFile=LICENSE" if os.path.exists("LICENSE") else ";LicenseFile=LICENSE  ; License file not found"
    
    inno_script = f'''[Setup]
AppName=Employee Face Registration & Tracking
AppVersion=1.0
AppPublisher=needyamin
AppPublisherURL=https://github.com/needyamin/employee-face-registration-and-tracking
AppSupportURL=https://github.com/needyamin/employee-face-registration-and-tracking/issues
AppUpdatesURL=https://github.com/needyamin/employee-face-registration-and-tracking
DefaultDirName={{autopf}}\\Employee Face Registration & Tracking
DefaultGroupName=Employee Face Registration & Tracking
AllowNoIcons=yes
{license_line}
OutputDir=installer
OutputBaseFilename=Employee_Face_Registration_Tracking_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\\Employee_Face_Registration_Tracking.exe"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "data.py"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "faces.db"; DestDir: "{{app}}"; Flags: ignoreversion; Check: FileExists

[Icons]
Name: "{{group}}\\Employee Face Registration & Tracking"; Filename: "{{app}}\\Employee_Face_Registration_Tracking.exe"
Name: "{{group}}\\{{cm:UninstallProgram,Employee Face Registration & Tracking}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\Employee Face Registration & Tracking"; Filename: "{{app}}\\Employee_Face_Registration_Tracking.exe"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\Employee Face Registration & Tracking"; Filename: "{{app}}\\Employee_Face_Registration_Tracking.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\Employee_Face_Registration_Tracking.exe"; Description: "{{cm:LaunchProgram,Employee Face Registration & Tracking}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
'''
    
    with open('setup.iss', 'w', encoding='utf-8') as f:
        f.write(inno_script)
    
    print("✓ Inno Setup script created")

def build_installer(inno_path):
    """Build installer using Inno Setup"""
    print("Building installer...")
    
    # Create installer directory
    if not os.path.exists('installer'):
        os.makedirs('installer')
    
    # Build installer
    cmd = [inno_path, "setup.iss"]
    try:
        subprocess.check_call(cmd)
        print("✓ Installer built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Installer build failed: {e}")
        return False

def create_portable_package():
    """Create portable package with executable and dependencies"""
    print("Creating portable package...")
    
    # Create portable directory
    portable_dir = "portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    os.makedirs(portable_dir)
    
    # Copy executable
    if os.path.exists("dist/Employee_Face_Registration_Tracking.exe"):
        shutil.copy2("dist/Employee_Face_Registration_Tracking.exe", portable_dir)
        
        # Copy additional files
        if os.path.exists("data.py"):
            shutil.copy2("data.py", portable_dir)
        if os.path.exists("faces.db"):
            shutil.copy2("faces.db", portable_dir)
        
        print("✓ Portable package created")
        return True
    else:
        print("✗ Executable not found")
        return False

def main():
    """Main build process"""
    print("Employee Face Registration & Tracking - Build Script")
    print("=" * 50)
    
    # Check if we're on Windows
    if sys.platform != "win32":
        print("✗ This build script is designed for Windows only")
        return False
    
    # Get user choice
    build_type = get_user_choice()
    
    # Step 1: Install requirements
    if not install_requirements():
        return False
    
    # Step 2: Check/install PyInstaller
    if not check_pyinstaller():
        return False
    
    # Step 3: Create spec file
    create_spec_file()
    
    # Step 4: Build executable
    if not build_executable():
        return False
    
    # Step 5: Handle build type
    if build_type == "installer":
        # Check for Inno Setup
        inno_path = check_inno_setup()
        if inno_path:
            create_inno_setup_script()
            if build_installer(inno_path):
                print("\n" + "=" * 50)
                print("INSTALLER BUILD COMPLETED SUCCESSFULLY!")
                print("=" * 50)
                print("\nFiles created:")
                print("- dist/Employee_Face_Registration_Tracking.exe (Portable executable)")
                print("- installer/Employee_Face_Registration_Tracking_Setup.exe (Installer)")
                print("\nTo install:")
                print("1. Run Employee_Face_Registration_Tracking_Setup.exe")
                print("2. Follow the installation wizard")
                print("\nTo run portable version:")
                print("- Double-click Employee_Face_Registration_Tracking.exe")
            else:
                print("Installer build failed, but portable executable is available.")
        else:
            print("Inno Setup not found. Creating portable package only.")
            create_portable_package()
    else:  # portable
        create_portable_package()
        print("\n" + "=" * 50)
        print("PORTABLE BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\nFiles created:")
        print("- portable/Employee_Face_Registration_Tracking.exe (Portable executable)")
        print("- portable/data.py (Data module)")
        print("- portable/faces.db (Database file, if exists)")
        print("\nTo run:")
        print("- Double-click Employee_Face_Registration_Tracking.exe")
    
    print("\nGitHub Repository:")
    print("https://github.com/needyamin/employee-face-registration-and-tracking")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nBuild failed. Please check the error messages above.")
        sys.exit(1) 