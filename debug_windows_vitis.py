#!/usr/bin/env python3
"""
Windows Vitis HLS Debug Script
This script helps diagnose the 3221225781 access violation error on Windows.
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil

def run_command(cmd, description):
    """Run a command and return success/failure with output."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"Return Code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        
        if result.returncode == 0:
            print("✅ SUCCESS")
            return True
        else:
            print("❌ FAILED")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 EXCEPTION: {e}")
        return False

def check_vitis_installation():
    """Check Vitis HLS installation and paths."""
    print("\n🔍 CHECKING VITIS HLS INSTALLATION")
    
    # Check if vitis_hls.exe exists in PATH
    vitis_hls_exe = shutil.which("vitis_hls.exe")
    if vitis_hls_exe:
        print(f"✅ Found vitis_hls.exe in PATH: {vitis_hls_exe}")
    else:
        print("❌ vitis_hls.exe not found in PATH")
    
    # Check common installation paths
    common_paths = [
        r"C:\Xilinx\2025.1\Vitis\bin\unwrapped\win64.o\vitis_hls.exe",
        r"C:\Xilinx\2024.2\Vitis\bin\unwrapped\win64.o\vitis_hls.exe",
        r"C:\Xilinx\2024.1\Vitis\bin\unwrapped\win64.o\vitis_hls.exe",
        r"C:\Xilinx\Vitis\2023.2\bin\vitis_hls.exe",
    ]
    
    for path in common_paths:
        if Path(path).exists():
            print(f"✅ Found Vitis HLS at: {path}")
            break
    else:
        print("❌ Vitis HLS not found in common paths")

def test_simple_compilation():
    """Test simple C++ compilation without Vitis HLS."""
    print("\n🔍 TESTING SIMPLE C++ COMPILATION")
    
    # Create a simple test file
    test_cpp = """
#include <iostream>
int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}
"""
    
    test_file = Path("test_simple.cpp")
    test_file.write_text(test_cpp)
    
    # Test with different compilers
    compilers = [
        ["g++", "test_simple.cpp", "-o", "test_simple.exe"],
        ["clang++", "test_simple.cpp", "-o", "test_simple_clang.exe"],
    ]
    
    for compiler_cmd in compilers:
        if shutil.which(compiler_cmd[0]):
            success = run_command(compiler_cmd, f"Simple compilation with {compiler_cmd[0]}")
            if success:
                # Test running the compiled program
                exe_name = compiler_cmd[-1]
                run_command([exe_name], f"Running {exe_name}")
        else:
            print(f"⚠️  {compiler_cmd[0]} not found in PATH")

def test_vitis_hls_basic():
    """Test basic Vitis HLS functionality."""
    print("\n🔍 TESTING VITIS HLS BASIC FUNCTIONALITY")
    
    # Test vitis_hls version
    vitis_hls_exe = shutil.which("vitis_hls.exe")
    if vitis_hls_exe:
        run_command([vitis_hls_exe, "-version"], "Vitis HLS version check")
    else:
        print("❌ Cannot test Vitis HLS - executable not found")

def test_vitis_hls_simple_project():
    """Test creating a simple Vitis HLS project."""
    print("\n🔍 TESTING VITIS HLS SIMPLE PROJECT")
    
    # Create a simple HLS test file
    hls_test_cpp = """
#include <ap_int.h>

ap_int<32> simple_function(ap_int<32> a, ap_int<32> b) {
    return a + b;
}
"""
    
    test_file = Path("test_hls.cpp")
    test_file.write_text(hls_test_cpp)
    
    # Create a simple TCL script
    tcl_script = """
open_project test_project
set_top simple_function
add_files test_hls.cpp
open_solution solution1 -flow_target vivado
set_part xc7z020clg484-1
create_clock -period 10 -name default
csynth_design
exit
"""
    
    tcl_file = Path("test_hls.tcl")
    tcl_file.write_text(tcl_script)
    
    # Test Vitis HLS with simple project
    vitis_hls_exe = shutil.which("vitis_hls.exe")
    if vitis_hls_exe:
        run_command([vitis_hls_exe, "-f", "test_hls.tcl"], "Simple Vitis HLS project")
    else:
        print("❌ Cannot test Vitis HLS project - executable not found")

def check_system_dependencies():
    """Check for missing system dependencies."""
    print("\n🔍 CHECKING SYSTEM DEPENDENCIES")
    
    # Check for Visual C++ redistributables
    dlls_to_check = [
        "msvcp140.dll",
        "vcruntime140.dll",
        "vcruntime140_1.dll",
    ]
    
    for dll in dlls_to_check:
        dll_path = shutil.which(dll)
        if dll_path:
            print(f"✅ Found {dll}: {dll_path}")
        else:
            print(f"❌ Missing {dll}")
    
    # Check Windows version
    import platform
    print(f"Windows Version: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")

def main():
    """Main diagnostic function."""
    print("🔧 WINDOWS VITIS HLS DIAGNOSTIC TOOL")
    print("This will help identify the cause of error code 3221225781")
    
    check_vitis_installation()
    check_system_dependencies()
    test_simple_compilation()
    test_vitis_hls_basic()
    test_vitis_hls_simple_project()
    
    print("\n" + "="*60)
    print("DIAGNOSTIC COMPLETE")
    print("="*60)
    print("\nCommon solutions for error 3221225781:")
    print("1. Install Microsoft Visual C++ Redistributable 2015-2022")
    print("2. Reinstall Vitis HLS with Windows-specific components")
    print("3. Check PATH environment variables")
    print("4. Run as Administrator")
    print("5. Disable antivirus temporarily")

if __name__ == "__main__":
    main()
