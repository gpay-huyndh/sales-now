# Công cụ lấy dữ liệu từ website công ty

**Ngôn ngữ:** [日本語](README.md) | [English](README.en.md) | Tiếng Việt (file này)

Crawl website chính thức của 10 công ty niêm yết bằng cách đi theo các liên kết, rồi dùng AI tạo sinh (LLM) để trích xuất **địa chỉ trụ sở chính, tên người đại diện, vốn điều lệ, tháng/năm thành lập**. Công cụ không dùng selector riêng cho từng site; việc xếp hạng link theo từ khóa giúp xử lý mọi site theo cùng một logic.

So sánh công nghệ và kết quả Bài B xem trong [report.vi.md](report.vi.md).

## Yêu cầu

- Python 3.9 trở lên
- API key của một nhà cung cấp LLM (Gemini / OpenAI / Anthropic), hoặc Ollama chạy local

## Cài đặt

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium        # dự phòng cho site render bằng JS
cp .env.example .env
```

Sửa `.env` để đặt model và API key.

```
LLM_MODEL=gemini/gemini-3.1-flash-lite
LLM_FALLBACK_MODEL=            # tùy chọn: dùng khi model chính lỗi
GEMINI_API_KEY=xxxxxxxx
```

Ví dụ giá trị `LLM_MODEL` (định dạng litellm): `gemini/gemini-3.1-flash-lite`, `gpt-4o-mini` (`OPENAI_API_KEY`), `anthropic/claude-3-5-haiku-latest` (`ANTHROPIC_API_KEY`), `ollama/llama3.1` (không cần key).

> [!NOTE]
> Model có thể bị ngưng cung cấp. Nếu gặp lỗi `404`, hãy đổi sang tên model hiện đang dùng được của nhà cung cấp.

## Cách chạy

```bash
# Cả 10 công ty (chạy qua CLI)
python src/main.py

# Một công ty (lọc theo một phần tên)
python src/main.py --only サカタ

# Duyệt nhiều trang hơn cho mỗi công ty (khi thiếu dữ liệu)
python src/main.py --max-pages 6
```

### Chạy qua giao diện (Streamlit - Phương án A)
Bạn có thể dùng giao diện web (hỗ trợ chuyển đổi Tiếng Anh, Việt, Nhật) để trích xuất từng công ty:
```bash
streamlit run src/app.py
```
Giao diện sẽ tự động mở tại `http://localhost:8501`.

### Chạy Phương án B (Next.js + Firecrawl + Vercel AI SDK)
Đây là dự án riêng trong thư mục `next-app`. Bạn cần cấu hình `FIRECRAWL_API_KEY` và `GEMINI_API_KEY` trong file `next-app/.env.local`.
```bash
cd next-app
npm install
npm run dev
```
Giao diện web hiện đại sẽ chạy ở `http://localhost:3000`.

Đầu vào là `input/companies.csv` (`name,url`).

### Bài B (khảo sát Indeed)

```bash
python src/indeed_probe.py
```

Gửi mỗi phương pháp 1 request (tổng 4 phương pháp) và lưu kết quả vào `result/indeed_probe.json` cùng ảnh chụp màn hình. Bước "headed" sẽ mở một cửa sổ Chrome thật; đừng đóng cho đến khi chạy xong.

### Chạy test

```bash
python -m pytest -q tests
```

## Kết quả đầu ra

| File | Nội dung |
|---|---|
| `result/companies.csv` | Dữ liệu trích xuất (UTF-8 BOM để mở bằng Excel) kèm model, token, chi phí, thời gian |
| `result/companies.json` | Như trên, thêm URL đã duyệt và kết quả kiểm tra bằng chứng |
| `result/run_log.json` | Tổng token, chi phí, thời gian và model thực sự trả lời |
| `result/indeed_probe.json` | Kết quả thí nghiệm Bài B |

## Cách hoạt động

1. Thu thập link từ trang chủ và, khi cần, từ các trang con (gồm cả subdomain cùng tên miền gốc).
2. Xếp hạng link theo từ khóa như 会社概要, 企業情報, corporate, profile.
3. Làm sạch văn bản của các trang đứng đầu và nhờ LLM trích xuất JSON (không có thì `null`, không đoán mò).
4. Kiểm tra đoạn trích dẫn bằng chứng có thật trong trang, và chuẩn hóa ngày thành lập sang `YYYY-MM`.
5. Nếu còn trường thiếu, bổ sung từ trang ứng viên tiếp theo.

## Cấu trúc thư mục

```
├── input/companies.csv   # danh sách công ty
├── prompts/              # lịch sử prompt đã dùng với AI tạo sinh
├── result/               # dữ liệu thu được
├── src/                  # mã nguồn
├── tests/                # unit test
├── README.md             # tiếng Nhật (đề bài yêu cầu)
├── README.en.md / README.vi.md
└── report.md / report.en.md / report.vi.md
```

## Hạn chế đã biết

- Gemini bản miễn phí bị giới hạn tốc độ (ví dụ 15 request/phút). Lỗi `429` có thể làm một số trường bị trống; hãy chạy lại riêng công ty đó bằng `--only`.
- Vốn điều lệ được giữ nguyên văn (ví dụ `30,685百万円`), chưa quy đổi về một đơn vị số.
- Độ đúng so với trang chính thức cần được kiểm tra riêng (Phụ lục A trong [report.vi.md](report.vi.md)).
- Không commit `.env` (đã có trong `.gitignore`).
