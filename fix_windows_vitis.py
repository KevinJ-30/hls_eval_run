#!/usr/bin/env python3
"""
Windows Vitis HLS Fix Script
Attempts to fix common issues causing error 3221225781.
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil

def fix_environment_variables():
    """Fix common environment variable issues."""
    print("🔧 FIXING ENVIRONMENT VARIABLES")
    
    # Get current PATH
    current_path = os.environ.get('PATH', '')
    print(f"Current PATH length: {len(current_path)}")
    
    # Add common Vitis paths if not present
    vitis_paths = [
        r"C:\Xilinx\2025.1\Vitis\bin\unwrapped\win64.o",
        r"C:\Xilinx\2025.1\Vitis\lib\win64.o",
        r"C:\Xilinx\2025.1\Vitis\win64\lib\csim",
        r"C:\Xilinx\2025.1\Vitis\win64\tools\clang-3.9-csynth\bin",
    ]
    
    new_paths = []
    for path in vitis_paths:
        if Path(path).exists() and path not in current_path:
            new_paths.append(path)
            print(f"✅ Adding to PATH: {path}")
    
    if new_paths:
        # Update PATH for current session
        os.environ['PATH'] = current_path + ';' + ';'.join(new_paths)
        print("✅ Updated PATH environment variable")
    else:
        print("ℹ️  No new paths to add")

def test_alternative_compiler():
    """Test using an alternative C++ compiler instead of Vitis HLS clang."""
    print("\n🔧 TESTING ALTERNATIVE COMPILER APPROACH")
    
    # Check if we have alternative compilers
    alternative_compilers = [
        "g++",
        "clang++",
        "msvc",
    ]
    
    available_compilers = []
    for compiler in alternative_compilers:
        if shutil.which(compiler):
            available_compilers.append(compiler)
            print(f"✅ Found alternative compiler: {compiler}")
    
    if not available_compilers:
        print("❌ No alternative compilers found")
        return False
    
    # Create a simple test
    test_cpp = """
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};
    int sum = 0;
    for (int x : vec) {
        sum += x;
    }
    std::cout << "Sum: " << sum << std::endl;
    return 0;
}
"""
    
    test_file = Path("test_alternative.cpp")
    test_file.write_text(test_cpp)
    
    # Test compilation with alternative compiler
    for compiler in available_compilers:
        print(f"\nTesting with {compiler}...")
        cmd = [compiler, "test_alternative.cpp", "-o", f"test_{compiler}.exe"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ {compiler} compilation successful")
                # Test running
                run_cmd = [f"test_{compiler}.exe"]
                run_result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=10)
                if run_result.returncode == 0:
                    print(f"✅ {compiler} execution successful: {run_result.stdout.strip()}")
                    return True
            else:
                print(f"❌ {compiler} compilation failed: {result.stderr}")
        except Exception as e:
            print(f"❌ {compiler} test failed: {e}")
    
    return False

def create_minimal_vitis_test():
    """Create a minimal Vitis HLS test to isolate the issue."""
    print("\n🔧 CREATING MINIMAL VITIS HLS TEST")
    
    # Create minimal HLS file
    hls_code = """
#include <ap_int.h>

ap_int<8> add(ap_int<8> a, ap_int<8> b) {
    return a + b;
}
"""
    
    hls_file = Path("minimal_hls.cpp")
    hls_file.write_text(hls_code)
    
    # Create minimal TCL script
    tcl_script = """
open_project minimal_test
set_top add
add_files minimal_hls.cpp
open_solution solution1 -flow_target vivado
set_part xc7z020clg484-1
create_clock -period 10 -name default
csynth_design
exit
"""
    
    tcl_file = Path("minimal_test.tcl")
    tcl_file.write_text(tcl_script)
    
    # Test with minimal setup
    vitis_hls_exe = shutil.which("vitis_hls.exe")
    if vitis_hls_exe:
        print("Testing minimal Vitis HLS project...")
        try:
            result = subprocess.run(
                [vitis_hls_exe, "-f", "minimal_test.tcl"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            print(f"Return code: {result.returncode}")
            if result.returncode == 0:
                print("✅ Minimal Vitis HLS test successful!")
                return True
            else:
                print(f"❌ Minimal test failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Minimal test timed out")
            return False
        except Exception as e:
            print(f"💥 Minimal test exception: {e}")
            return False
    else:
        print("❌ Vitis HLS executable not found")
        return False

def suggest_workarounds():
    """Suggest workarounds for the Windows issue."""
    print("\n" + "="*60)
    print("SUGGESTED WORKAROUNDS")
    print("="*60)
    
    print("\n1. 🚀 IMMEDIATE WORKAROUNDS:")
    print("   - Run Command Prompt as Administrator")
    print("   - Temporarily disable antivirus")
    print("   - Try running in a clean environment")
    
    print("\n2. 🔧 SYSTEM FIXES:")
    print("   - Install Microsoft Visual C++ Redistributable 2015-2022")
    print("   - Update Windows to latest version")
    print("   - Check for Windows updates")
    
    print("\n3. 🛠️ VITIS HLS FIXES:")
    print("   - Reinstall Vitis HLS")
    print("   - Install Vitis HLS with Windows-specific components")
    print("   - Try different Vitis HLS version")
    
    print("\n4. 🔄 ALTERNATIVE APPROACHES:")
    print("   - Use WSL2 (Windows Subsystem for Linux)")
    print("   - Use a Linux VM")
    print("   - Use a different machine with Linux")
    
    print("\n5. 📝 CODE MODIFICATIONS:")
    print("   - Modify the pipeline to skip Vitis HLS steps")
    print("   - Use alternative C++ compilers")
    print("   - Implement a Windows-specific fallback")

def main():
    """Main fix function."""
    print("🔧 WINDOWS VITIS HLS FIX TOOL")
    print("Attempting to fix error 3221225781")
    
    # Try fixes
    fix_environment_variables()
    
    # Test alternatives
    alternative_works = test_alternative_compiler()
    
    # Test minimal Vitis
    vitis_works = create_minimal_vitis_test()
    
    print("\n" + "="*60)
    print("FIX ATTEMPT RESULTS")
    print("="*60)
    
    if vitis_works:
        print("✅ Vitis HLS is working with minimal test")
        print("   The issue might be with the specific project configuration")
    elif alternative_works:
        print("✅ Alternative compilers work")
        print("   Consider modifying the pipeline to use alternative compilers")
    else:
        print("❌ Both Vitis HLS and alternatives failed")
        print("   This suggests a deeper system-level issue")
    
    suggest_workarounds()

if __name__ == "__main__":
    main()
