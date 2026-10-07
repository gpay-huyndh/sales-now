# AI Agent Conversation Log (Generative AI Usage)

Đây là tài liệu ghi nhận lịch sử các câu lệnh (prompts) mà người dùng đã giao cho AI Assistant (Agentic AI) trong suốt quá trình phát triển **Phương án A (Python + Playwright + LLM + Streamlit)**. AI Assistant đã tự động code, tạo cấu trúc thư mục, debug, và tối ưu hóa dựa trên các yêu cầu này.

## Phiên 1: Phân tích yêu cầu và Đề xuất Giải pháp
- **User Prompt:**
  > "@[Scraping_Test_Nguyen_Dang_Hong_Huy_EN.md] làm báo cáo theo yêu cầu"
  > "có bảng tiếng anh"
  > "@[README.md], @[report.md] tách riêng thành 3 version anh, việt, nhật"
- **AI Response/Action:**
  Phân tích yêu cầu bài test, đề xuất thiết kế kiến trúc hệ thống, chia ra làm 2 phương án (Phương án A: Python, Phương án B: TypeScript). Tách các file README.md, report.md thành 3 ngôn ngữ theo yêu cầu.

## Phiên 2: Xây dựng Phương án A và Giao diện Streamlit
- **User Prompt:**
  > "A. Python + Playwright/httpx + BS4 + LLM (đã chọn) => tôi muốn có UI trực quan hơn"
  > "update tài liệu hướng dẫn cho tất cà version anh, việt, nhật. streamlit nên để switch 3 ngôn ngữ"
- **AI Response/Action:**
  Khởi tạo `src/app.py` bằng Streamlit. Thiết kế giao diện trực quan hiển thị thông tin trích xuất. Cập nhật hệ thống dịch đa ngôn ngữ cho UI (Tiếng Anh, Tiếng Việt, Tiếng Nhật). Cập nhật toàn bộ tài liệu hướng dẫn để tích hợp cách chạy Streamlit.

## Phiên 3: Bổ sung tính năng Batch Processing & Export
- **User Prompt:**
  > "Streamlit load default input này @[/Users/huyndh/Desktop/test/sales-now/input/companies.csv] cho end user nhập tay/ pick chạy từng cái hoặc hàng loạt"
  > "cho phép export kết quả"
- **AI Response/Action:**
  Cấu trúc lại `src/app.py` thành 3 Tab (Nhập thủ công, Chọn danh sách, Chạy hàng loạt). Tích hợp logic xử lý hàng loạt vào Streamlit, bổ sung Progress Bar. Bổ sung tính năng xuất kết quả ra định dạng `.csv` và `.json` ở cuối quá trình.

## Phiên 4: Tinh chỉnh Trải nghiệm Người dùng (UX) và Code Quality
- **User Prompt:**
  > "nhân lưu csv / json thì màn hình bị reset, tôi muốn giữ trạng thái, default là tiếng nhật"
  > "tôi ko làm phương án b nữa, bây giờ tôi muốn clean code cho phương án A"
- **AI Response/Action:**
  - Sửa lỗi UX của Streamlit bằng cách lưu kết quả vào `st.session_state` để ngăn việc màn hình bị reset khi user click nút Tải về (Export).
  - Thay đổi ngôn ngữ mặc định sang Tiếng Nhật ở sidebar UI.
  - Sử dụng công cụ `ruff` để tự động định dạng (format) và fix lints (PEP-8) toàn bộ thư mục `src/`, đảm bảo mã nguồn Phương án A hoàn toàn "sạch" và đạt chuẩn production.
