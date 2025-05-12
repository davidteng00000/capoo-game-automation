import sys
import os
import traceback # 用於打印更詳細的錯誤信息

print("--- Minimal Import Test ---")
print(f"Python Executable: {sys.executable}") 

try:
    # 嘗試導入整個套件
    import pyscrcpy
    print("Import 'pyscrcpy' successful!")
    # 嘗試打印版本號 (如果導入成功)
    print(f"Version: {getattr(pyscrcpy, '__version__', 'N/A')}") # 使用 getattr 更安全

    # 嘗試導入特定的類別
    from pyscrcpy import Client 
    print("Import 'ScrcpyClient' from 'pyscrcpy' successful!")

except ImportError as e:
    print(f"\n!!! ImportError occurred: {e} !!!")
    print("Traceback:")
    traceback.print_exc() # 打印完整的導入錯誤追溯

except Exception as e:
    print(f"\n!!! An unexpected error occurred: {e} !!!")
    print("Traceback:")
    traceback.print_exc() # 打印完整的其他錯誤追溯

print("---------------------------")