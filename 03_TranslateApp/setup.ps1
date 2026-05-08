# TranslatorApp v1.0 Setup Script
# Tự động cài đặt môi trường và thư viện cần thiết

Write-Host "--- TranslatorApp Setup ---" -ForegroundColor Cyan

# 1. Kiểm tra Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Lỗi: Không tìm thấy Python. Vui lòng cài đặt Python 3.10+ trước." -ForegroundColor Red
    exit
}

Write-Host "Đang kiểm tra phiên bản Python..."
python --version

# 2. Cài đặt thư viện
Write-Host "Đang cài đặt các thư viện phụ thuộc từ requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nThành công! Mọi thứ đã sẵn sàng." -ForegroundColor Green
    Write-Host "Bạn có thể khởi động ứng dụng bằng lệnh: python main.py" -ForegroundColor Cyan
} else {
    Write-Host "`nĐã có lỗi xảy ra trong quá trình cài đặt." -ForegroundColor Red
}

Write-Host "`nNhấn phím bất kỳ để thoát..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
