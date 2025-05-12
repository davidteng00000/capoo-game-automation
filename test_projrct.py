import sys
import os
print("--- Debug Info ---")
print(f"正在使用的 Python: {sys.executable}") 
print("正在搜尋的套件路徑 (sys.path):")
for path in sys.path:
    print(f"  {path}")
print("------------------")

import cv2
import time
import traceback

# 嘗試導入 pyscrcpy，如果失敗則提示安裝
try:
    from pyscrcpy import Client
except ImportError:
    print("錯誤：找不到 pyscrcpy 套件。")
    print("請先在您的 Python 環境中安裝它： pip install pyscrcpy")
    print("同時，請確保您的電腦上已經安裝了 'adb' 和 'scrcpy' 這兩個命令列工具，並且它們可以被您的環境找到。")
    exit()

# 設定顯示視窗的標題
WINDOW_TITLE = "Android Screen Mirror (Press 'q' to quit)"

def main():
    client = None # 初始化 client 變數
    print("正在嘗試連接到 Android 設備並啟動螢幕鏡像...")
    
    try:
        # 初始化 ScrcpyClient，device=None 會自動選擇第一個偵測到的設備
        client = Client(device=None, max_fps=30) 
        print("ScrcpyClient 初始化完成。")

        # 在背景執行緒中啟動 scrcpy 串流
        client.start(threaded=True)
        print("Scrcpy 影像串流已在背景啟動。")
        
        # 等待串流稍微穩定
        time.sleep(2) 
        print(f"將在視窗 '{WINDOW_TITLE}' 中顯示串流畫面。")
        print("提示：請在顯示畫面的視窗中按下 'q' 鍵來結束程式。")
        print("\n*** 重要提示 (WSL 用戶) ***")
        print("如果您在 WSL (Windows Subsystem for Linux) 環境中執行此腳本：")
        print(" - 除非您使用 Windows 11 的 WSLg 功能，或已手動配置 X Server，")
        print(f" - 否則 '{WINDOW_TITLE}' 視窗可能無法正常顯示，甚至可能導致腳本崩潰。")
        print("如果視窗未出現或程式崩潰，請檢查您的 WSL 圖形介面支援設定。")
        print("*" * 30)

        while True:
            # 從串流獲取最新的畫面幀 (NumPy Array, BGR 格式)
            frame = client.get_frame()

            if frame is not None:
                # 如果成功獲取到畫面幀，就顯示它
                cv2.imshow(WINDOW_TITLE, frame)
            else:
                # 如果暫時沒獲取到畫面，檢查一下 scrcpy 是否還在運行
                if client and not client.alive:
                    print("偵測到 Scrcpy client 已經停止運行。")
                    break 
                # 短暫等待，避免 CPU 空轉
                time.sleep(0.01) 

            # 檢查是否有按下 'q' 鍵，如果按下就退出循環
            # cv2.waitKey(1) 等待 1 毫秒的按鍵輸入，並返回按鍵碼
            # & 0xFF 是為了確保在不同系統上都能正確獲取按鍵碼
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("偵測到 'q' 鍵，正在停止程式...")
                break

    except KeyboardInterrupt:
        # 處理 Ctrl+C 中斷
        print("\n接收到 Ctrl+C，正在停止程式...")
    except Exception as e:
        # 處理其他可能的錯誤
        print(f"\n程式執行過程中發生錯誤：{e}")
        traceback.print_exc() # 打印詳細的錯誤追溯信息
    finally:
        # 無論是正常退出還是發生錯誤，最後都要確保資源被釋放
        print("正在清理資源...")
        if client and client.alive:
            print("正在停止 Scrcpy client...")
            client.stop() # 停止 scrcpy 串流
        cv2.destroyAllWindows() # 關閉所有 OpenCV 創建的視窗
        print("程式已結束。")

# --- 程式進入點 ---
if __name__ == '__main__':
    print("--- 前置條件檢查提醒 ---")
    print("請確保：")
    print("1. 您的 Android 手機已透過 USB 線連接到電腦。")
    print("2. 手機已啟用「開發人員選項」和「USB 偵錯」模式。")
    print("3. 當手機連接時，您已在手機上「允許」這台電腦進行 USB 偵錯。")
    print("4. 您的電腦上已安裝 'adb' 命令列工具，並且可以在終端機執行。")
    print("5. 您的電腦上已安裝 'scrcpy' 命令列工具，並且可以在終端機執行。")
    print("6. 您已在目前的 Python 環境中安裝 'pyscrcpy' 和 'opencv-python' 套件。")
    print("-" * 20)
    
    main() # 執行主函數