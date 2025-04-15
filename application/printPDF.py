import subprocess
import os
import win32print
import time
import sys

timeout = 7

def print_pdf(pdf_path, printer_name="Bluetooth PT-210", paper_size="ZPrinter Paper(領収サイズ)", exe_path="application/pdftoprinter/PDFtoPrinter.exe"):
    # パスを絶対パスに変換（安全策）
    pdf_path = os.path.abspath(pdf_path)
    exe_path = os.path.abspath(exe_path)

    try:
        # 印刷実行
        cmd = [
            exe_path,
            f"/PaperSize:{paper_size}",
            "/NoConfirm",
            pdf_path,
            printer_name
        ]
        subprocess.run(cmd , check=True)

        print("印刷コマンド送信成功。ジョブ監視開始…")

        # プリンターハンドルを取得
        hPrinter = win32print.OpenPrinter(printer_name)
        start_time = time.time()

        while time.time() - start_time < timeout:
            jobs = win32print.EnumJobs(hPrinter, 0, 99, 1)
            if not jobs:
                print("印刷完了（ジョブキューが空）")
                win32print.ClosePrinter(hPrinter)
                return True

            # すべてのジョブのステータスを確認
            all_done = all(job["Status"] in [0, 0x00000080] for job in jobs)
            if all_done:
                print("すべてのジョブが完了ステータスです")
                win32print.ClosePrinter(hPrinter)
                return True

            time.sleep(0.5)

        print("印刷が完了しなかったか、タイムアウトしました")
        # タイムアウト：未処理ジョブが残っている → キャンセル
        print("タイムアウト！未完了ジョブをキャンセルします")
        for job in win32print.EnumJobs(hPrinter, 0, 99, 1):
            job_id = job["JobId"]
            print(f"キャンセル中: ジョブID {job_id}")
            win32print.SetJob(hPrinter, job_id, 0, None, win32print.JOB_CONTROL_DELETE)
        
        win32print.ClosePrinter(hPrinter)
        os.remove(pdf_path)
        return False

    except Exception as e:
        print(f"印刷処理中にエラーが発生: {e}")
        for job in win32print.EnumJobs(hPrinter, 0, 99, 1):
            job_id = job["JobId"]
            print(f"キャンセル中: ジョブID {job_id}")
            win32print.SetJob(hPrinter, job_id, 0, None, win32print.JOB_CONTROL_DELETE)
        
        win32print.ClosePrinter(hPrinter)
        os.remove(pdf_path)
        return False

if __name__ == '__main__':
    print_pdf("reciept_files/20250411001.pdf")