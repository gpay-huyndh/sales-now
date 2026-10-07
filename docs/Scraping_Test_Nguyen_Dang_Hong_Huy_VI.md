**Hãy dịch yêu cầu này từ tiếng Nhật và trả lời.**

# **【Bài tập Web Scraping và Trích xuất dữ liệu】**

## **1. Tổng quan**

Bài kiểm tra này là một bài thi thực hành nhằm đánh giá khả năng thu thập dữ liệu trong thực tế, quy trình suy nghĩ khi lựa chọn công nghệ, và kỹ năng sử dụng AI tạo sinh (Generative AI) một cách hiệu quả. Vui lòng nộp bài theo phương thức được chỉ định trong vòng 9 giờ kể từ thời gian bắt đầu. Bài làm sẽ được đánh giá dựa trên nội dung commit tại thời điểm được chỉ định. Ngay cả khi chưa hoàn thành trong thời gian quy định, chúng tôi vẫn sẽ đánh giá quy trình tiếp cận của bạn, vì vậy hãy commit những phần đã hoàn thành trước thời hạn.

## **2. Bài tập A: Lấy dữ liệu từ trang web của công ty**

Sử dụng danh sách URL của 10 công ty niêm yết dưới đây làm đầu vào (input), thu thập dữ liệu (scrape) trang web chính thức của từng công ty bằng cách theo các liên kết, và sử dụng AI tạo sinh để trích xuất các dữ liệu được chỉ định. Vì mỗi trang web có thiết kế và cấu trúc khác nhau, hãy xây dựng một giải pháp có tính linh hoạt cao. Hướng dẫn cách thiết lập và cách chạy môi trường đã tạo bằng tiếng Nhật trong tệp `README.md`.

* **Trang web mục tiêu:**

| Tên công ty | URL |
| ----- | ----- |
| Nissui | [https://www.nissui.co.jp/](https://www.nissui.co.jp/) |
| Umios | [https://www.umios.com/](https://www.umios.com/) |
| Yukiguni Factory | [https://www.yukiguni-factory.co.jp/](https://www.yukiguni-factory.co.jp/) |
| Sakata Seed | [https://www.sakataseed.co.jp/](https://www.sakataseed.co.jp/) |
| Hokto | [https://www.hokto-kinoko.co.jp/](https://www.hokto-kinoko.co.jp/) |
| Sho-Bond Holdings | [https://www.sho-bondhd.jp/](https://www.sho-bondhd.jp/) |
| Mirait One | [https://www.mirait-one.com/](https://www.mirait-one.com/) |
| Tama Home | [https://www.tamahome.jp/](https://www.tamahome.jp/) |
| Kyokuyo | [https://www.kyokuyo.co.jp/](https://www.kyokuyo.co.jp/) |
| Nippon Aqua | [https://www.n-aqua.jp/](https://www.n-aqua.jp/) |

* **Dữ liệu cần trích xuất:** Địa chỉ trụ sở chính, Tên người đại diện, Vốn điều lệ, Tháng năm thành lập

## **3. Bài tập B: Thử thách với trang web có tính năng chống Bot 【Điểm cộng / Không bắt buộc】**

(Chỉ dành cho những ai đã hoàn thành hoàn toàn Bài tập A) Hãy thử thách lấy dữ liệu từ các trang web chặn các phương pháp scraping thông thường.

* **Trang mục tiêu:** [https://vn.indeed.com/jobs?q=remote](https://vn.indeed.com/jobs?q=remote)
* **Nội dung báo cáo (ghi trong `report.md`):**
  * Trang web đang sử dụng những biện pháp chống Bot nào?
  * Bạn đã thử áp dụng phương pháp nào để đối phó và kết quả ra sao?

## **4. Lựa chọn công nghệ và so sánh các phương pháp tiếp cận**

Khi thu thập dữ liệu, hãy xem xét và so sánh nhiều phương pháp khác nhau (các loại thư viện, framework, công cụ no-code, sử dụng API của AI tạo sinh, v.v.).
  Ví dụ: Python + Playwright + LangChain, TypeScript + Firecrawl + Vercel AI SDK, Dify, n8n.
Khi so sánh, hãy đánh giá chủ yếu dựa trên 3 tiêu chí dưới đây và giải thích lý do lựa chọn của bạn vào tệp `report.md`.

* **Chi phí (Cost):** Thời gian phát triển, chi phí cơ sở hạ tầng, phí sử dụng công cụ, v.v.
* **Tốc độ (Speed):** Tốc độ phát triển và tốc độ thực thi lấy dữ liệu.
* **Chất lượng / Độ toàn diện (Quality / Completeness):** Độ chính xác của dữ liệu và mức độ ít bỏ sót.

## **5. Về việc sử dụng AI tạo sinh (Generative AI)**

Trong bài tập này, bạn **được phép tự do sử dụng** các AI tạo sinh như ChatGPT, Claude, GitHub Copilot, v.v.
Tuy nhiên, bạn phải tuân thủ điều kiện sau:
⚠️ **Điều kiện bắt buộc:** Nếu bạn sử dụng các AI dạng chat như ChatGPT hay Claude, vui lòng nộp lịch sử của prompt và câu trả lời (hoặc liên kết chia sẻ).

## **6. Phương thức nộp bài**

Toàn bộ sản phẩm phải được nộp qua **GitHub**.

1. **Tạo repository:** Hãy tạo một private repository.
2. **Cấp quyền truy cập:** Mời 2 tài khoản GitHub ID được chỉ định của công ty chúng tôi làm collaborator:
   * atsunori0406
   * salesnow-tomohiro
3. **Cấu trúc thư mục (Khuyến nghị):** Sắp xếp repository của bạn như sau:
   `├── prompts/      # Lịch sử prompt đã sử dụng cho AI (định dạng txt)`
   `├── result/       # Dữ liệu thu thập được (định dạng CSV hoặc JSON)`
   `├── src/          # Toàn bộ mã nguồn (source code) đã tạo`
   `├── README.md     # Tài liệu hướng dẫn thiết lập và thực thi`
   `└── report.md     # Bảng so sánh lựa chọn công nghệ, và kết quả thảo luận phần B`

## **7. Tiêu chí đánh giá**

* **Khả năng hiểu:** Bạn có hiểu đúng bản chất của bài tập hay không.
* **Khả năng thiết kế:** Việc lựa chọn công nghệ có phù hợp khi cân nhắc về chi phí, tốc độ và chất lượng hay không.
* **Khả năng sử dụng AI:** Bạn có sử dụng AI tạo sinh một cách hiệu quả và xây dựng quy trình (flow) phù hợp hay không.
* **Khả năng viết tài liệu:** Tài liệu viết ra có dễ hiểu đối với bên thứ ba hay không.
