# 台股收盤行情通知 (6838 台新藥)

GitHub Actions 定時抓取 6838 台新藥 收盤行情並寄送至信箱。

## 排程時間

- **執行時間**: 週一至週五 台灣時間 13:35
- **觸發時機**: 台股收盤 (13:30) 後 5 分鐘

## 部署步驟

### 1. 推送到 GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/<你的帳號>/tw-stock-notify.git
git push -u origin main
```

### 2. 設定 GitHub Secrets

到 GitHub 專頁 → **Settings** → **Secrets and variables** → **Actions** → 新增以下 secrets：

| Secret            | 說明                                    |
|-------------------|----------------------------------------|
| `SMTP_SERVER`     | SMTP 伺服器（預設 `smtp.gmail.com`）    |
| `SMTP_PORT`       | 連接埠（預設 `587`）                     |
| `EMAIL_FROM`      | 寄件者 Gmail 地址                       |
| `EMAIL_PASSWORD`  | Gmail 應用程式密碼（非普通密碼）         |
| `EMAIL_TO`        | 收件者信箱（`motorgp2004@icloud.com`）   |

### 3. Gmail 應用程式密碼設定

1. 前往 https://myaccount.google.com/security
2. 開啟 **兩步驟驗證**
3. 到 **應用程式密碼** 產生一組密碼
4. 將該密碼設為 `EMAIL_PASSWORD` Secret

### 手動觸發測試

在 GitHub Actions 頁面點選 **Run workflow** 即可立即執行。
