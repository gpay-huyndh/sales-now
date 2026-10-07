import csv
import sys
import time
from pathlib import Path

import pandas as pd
import streamlit as st

# Add src to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from extractor import model_name
from main import process

st.set_page_config(
    page_title="Sales Now - Company Scraper", page_icon="🏢", layout="wide"
)


# Load companies
@st.cache_data
def load_companies():
    csv_path = ROOT / "input" / "companies.csv"
    if not csv_path.exists():
        return []
    with open(csv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


companies = load_companies()
company_options = {
    f"{c['name']} - {c['url']}": c for c in companies if c.get("name") and c.get("url")
}

# Translations
TRANSLATIONS = {
    "vi": {
        "title": "🏢 Sales Now - Company Scraper (Option A)",
        "desc": "Giao diện Streamlit cho pipeline trích xuất dữ liệu công ty bằng Python + Playwright + LLM.",
        "config": "Cấu hình",
        "max_pages": "Số trang tối đa (max_pages)",
        "model": "Mô hình hiện tại:",
        "tab_manual": "Nhập thủ công",
        "tab_pick": "Chọn từ danh sách",
        "tab_batch": "Chạy hàng loạt",
        "company_name": "Tên công ty",
        "company_name_ph": "VD: サカタのタネ",
        "company_url": "Website (URL)",
        "company_url_ph": "VD: https://www.sakataseed.co.jp/",
        "select_company": "Chọn công ty từ danh sách CSV",
        "extract_btn": "Trích xuất thông tin",
        "extract_batch_btn": "Chạy trích xuất hàng loạt",
        "err_empty": "Vui lòng nhập đầy đủ tên công ty và URL.",
        "spinner": "Đang thu thập và phân tích dữ liệu... (Vui lòng đợi vài giây)",
        "spinner_batch": "Đang chạy hàng loạt... (Tiến độ: {current}/{total})",
        "err_extract": "Không thể trích xuất dữ liệu.",
        "success": "Hoàn thành trong {time} giây!",
        "success_batch": "Hoàn thành chạy hàng loạt trong {time} giây!",
        "result_title": "Kết quả trích xuất",
        "fields": ["Địa chỉ trụ sở", "Người đại diện", "Chức danh", "Vốn điều lệ", "Ngày thành lập"],
        "status_ok": "✅",
        "status_warn": "⚠️ (Không thấy trên trang)",
        "status_err": "❌ (Trống)",
        "col_field": "Trường dữ liệu",
        "col_val": "Giá trị",
        "col_status": "Trạng thái",
        "extra_info": "Thông tin chi tiết (Pages & LLM)",
        "source": "Nguồn (Source URL):",
        "pages_count": "Số trang đã quét:",
        "pages_visited": "Trang đã thăm:",
        "tokens": "Số token:",
        "cost": "Chi phí ước tính:",
        "err_unknown": "Đã xảy ra lỗi:",
        "found_companies": "Tìm thấy **{count}** công ty trong file CSV.",
        "no_data_csv": "Không có dữ liệu trong file CSV.",
        "error_company": "Lỗi ở công ty {comp}: {err}"
    },
    "en": {
        "title": "🏢 Sales Now - Company Scraper (Option A)",
        "desc": "Streamlit UI for company data extraction pipeline using Python + Playwright + LLM.",
        "config": "Configuration",
        "max_pages": "Max pages to crawl",
        "model": "Current Model:",
        "tab_manual": "Manual Input",
        "tab_pick": "Pick from List",
        "tab_batch": "Batch Processing",
        "company_name": "Company Name",
        "company_name_ph": "e.g. サカタのタネ",
        "company_url": "Website (URL)",
        "company_url_ph": "e.g. https://www.sakataseed.co.jp/",
        "select_company": "Select company from CSV list",
        "extract_btn": "Extract Information",
        "extract_batch_btn": "Run Batch Extraction",
        "err_empty": "Please enter both company name and URL.",
        "spinner": "Scraping and analyzing data... (Please wait a few seconds)",
        "spinner_batch": "Running batch processing... (Progress: {current}/{total})",
        "err_extract": "Could not extract data.",
        "success": "Completed in {time} seconds!",
        "success_batch": "Batch processing completed in {time} seconds!",
        "result_title": "Extraction Results",
        "fields": ["Head Office Address", "Representative Name", "Representative Title", "Capital", "Established Date"],
        "status_ok": "✅",
        "status_warn": "⚠️ (Not found on page)",
        "status_err": "❌ (Empty)",
        "col_field": "Data Field",
        "col_val": "Value",
        "col_status": "Status",
        "extra_info": "Detailed Info (Pages & LLM)",
        "source": "Source URL:",
        "pages_count": "Pages Scanned:",
        "pages_visited": "Pages Visited:",
        "tokens": "Tokens:",
        "cost": "Estimated Cost:",
        "err_unknown": "An error occurred:",
        "found_companies": "Found **{count}** companies in the CSV file.",
        "no_data_csv": "No data found in the CSV file.",
        "error_company": "Error at company {comp}: {err}"
    },
    "ja": {
        "title": "🏢 Sales Now - 企業情報スクレイパー (Option A)",
        "desc": "Python + Playwright + LLMを使用した企業データ抽出パイプラインのStreamlit UI。",
        "config": "設定",
        "max_pages": "最大クロールページ数",
        "model": "現在のモデル:",
        "tab_manual": "手動入力",
        "tab_pick": "リストから選択",
        "tab_batch": "一括処理",
        "company_name": "企業名",
        "company_name_ph": "例: サカタのタネ",
        "company_url": "ウェブサイト (URL)",
        "company_url_ph": "例: https://www.sakataseed.co.jp/",
        "select_company": "CSVリストから企業を選択",
        "extract_btn": "情報を抽出",
        "extract_batch_btn": "一括抽出を実行",
        "err_empty": "企業名とURLの両方を入力してください。",
        "spinner": "データをスクレイピングして分析しています...（数秒お待ちください）",
        "spinner_batch": "一括処理を実行中... (進捗: {current}/{total})",
        "err_extract": "データを抽出できませんでした。",
        "success": "{time}秒で完了しました！",
        "success_batch": "一括処理が{time}秒で完了しました！",
        "result_title": "抽出結果",
        "fields": ["本社所在地", "代表者名", "役職", "資本金", "設立年月"],
        "status_ok": "✅",
        "status_warn": "⚠️ (ページ内に見つかりません)",
        "status_err": "❌ (空)",
        "col_field": "データ項目",
        "col_val": "値",
        "col_status": "ステータス",
        "extra_info": "詳細情報 (ページ & LLM)",
        "source": "情報源 (URL):",
        "pages_count": "スキャンしたページ数:",
        "pages_visited": "訪問したページ:",
        "tokens": "トークン数:",
        "cost": "推定コスト:",
        "err_unknown": "エラーが発生しました:",
        "found_companies": "CSVファイルに**{count}**社の企業が見つかりました。",
        "no_data_csv": "CSVファイルにデータがありません。",
        "error_company": "企業 {comp} のエラー: {err}"
    },
}

# Sidebar settings
lang_choice = st.sidebar.selectbox(
    "Language / Ngôn ngữ / 言語", ["English", "Tiếng Việt", "日本語"], index=2
)
lang_map = {"English": "en", "Tiếng Việt": "vi", "日本語": "ja"}
lang = lang_map[lang_choice]
t = TRANSLATIONS[lang]

st.title(t["title"])
st.markdown(t["desc"])

st.sidebar.header(t["config"])
max_pages = st.sidebar.slider(t["max_pages"], min_value=1, max_value=10, value=4)
st.sidebar.markdown(f"**{t['model']}** `{model_name()}`")

# Initialize session state for keeping results
if "manual_result" not in st.session_state:
    st.session_state.manual_result = None
if "pick_result" not in st.session_state:
    st.session_state.pick_result = None
if "batch_results" not in st.session_state:
    st.session_state.batch_results = None


def render_result(result):
    fields_keys = [
        "head_office_address",
        "representative_name",
        "representative_title",
        "capital",
        "established",
    ]
    labels = t["fields"]

    data = []
    for f, l in zip(fields_keys, labels):
        val = result.get(f)
        verified = result.get("verified", {}).get(f)
        status = (
            t["status_ok"]
            if verified
            else (t["status_warn"] if val else t["status_err"])
        )
        data.append(
            {
                t["col_field"]: l,
                t["col_val"]: val if val else "-",
                t["col_status"]: status,
            }
        )

    df = pd.DataFrame(data)
    st.table(df)

    with st.expander(t["extra_info"]):
        st.write(f"**{t['source']}** {result.get('source_url', 'None')}")
        st.write(f"**{t['pages_count']}** {result.get('pages_count', 0)}")
        st.write(
            f"**{t['pages_visited']}** {', '.join(result.get('pages_visited', []))}"
        )
        st.write(f"**LLM:** {result.get('model', 'Unknown')}")
        st.write(
            f"**{t['tokens']}** Input: {result.get('prompt_tokens', 0)}, Output: {result.get('completion_tokens', 0)}"
        )
        st.write(f"**{t['cost']}** ${result.get('cost_usd', 0.0):.6f}")
        st.json(result)

    # Export Buttons for Single Result
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        csv_data = pd.DataFrame([result]).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export CSV",
            data=csv_data,
            file_name=f"{result.get('company', 'company')}.csv",
            mime="text/csv",
        )
    with col2:
        import json

        json_data = json.dumps([result], ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 Export JSON",
            data=json_data,
            file_name=f"{result.get('company', 'company')}.json",
            mime="application/json",
        )


# Tabs
tab1, tab2, tab3 = st.tabs([t["tab_manual"], t["tab_pick"], t["tab_batch"]])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        manual_name = st.text_input(
            t["company_name"], placeholder=t["company_name_ph"], key="man_name"
        )
    with col2:
        manual_url = st.text_input(
            t["company_url"], placeholder=t["company_url_ph"], key="man_url"
        )

    if st.button(t["extract_btn"], key="btn_manual", type="primary"):
        if not manual_name or not manual_url:
            st.error(t["err_empty"])
        else:
            with st.spinner(t["spinner"]):
                try:
                    start_time = time.time()
                    result = process(manual_name, manual_url, max_pages)
                    if not result:
                        st.error(t["err_extract"])
                    else:
                        result["_duration"] = result.get(
                            "seconds", round(time.time() - start_time, 1)
                        )
                        st.session_state.manual_result = result
                except Exception as e:  # noqa: BLE001
                    st.error(f"{t['err_unknown']} {e}")
                    
    if st.session_state.manual_result:
        res = st.session_state.manual_result
        st.success(t["success"].replace("{time}", str(res.get("_duration", 0))))
        st.subheader(t["result_title"])
        render_result(res)

with tab2:
    selected_option = st.selectbox(t["select_company"], list(company_options.keys()))
    if st.button(t["extract_btn"], key="btn_pick", type="primary"):
        if not selected_option:
            st.error(t["err_empty"])
        else:
            comp = company_options[selected_option]
            with st.spinner(t["spinner"]):
                try:
                    start_time = time.time()
                    result = process(comp["name"], comp["url"], max_pages)
                    if not result:
                        st.error(t["err_extract"])
                    else:
                        result["_duration"] = result.get(
                            "seconds", round(time.time() - start_time, 1)
                        )
                        st.session_state.pick_result = result
                except Exception as e:  # noqa: BLE001
                    st.error(f"{t['err_unknown']} {e}")
                    
    if st.session_state.pick_result:
        res = st.session_state.pick_result
        st.success(t["success"].replace("{time}", str(res.get("_duration", 0))))
        st.subheader(f"{t['result_title']} - {res.get('company', '')}")
        render_result(res)

with tab3:
    st.write(t["found_companies"].replace("{count}", str(len(company_options))))
    if st.button(t["extract_batch_btn"], key="btn_batch", type="primary"):
        if not company_options:
            st.warning(t["no_data_csv"])
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()

            batch_results = []
            start_time = time.time()
            total = len(company_options)

            comps = list(company_options.values())
            for idx, comp in enumerate(comps):
                status_text.text(
                    t["spinner_batch"]
                    .replace("{current}", str(idx + 1))
                    .replace("{total}", str(total))
                    + f" ({comp['name']})"
                )
                try:
                    result = process(comp["name"], comp["url"], max_pages)
                    if result:
                        batch_results.append(result)
                except Exception as e:  # noqa: BLE001
                    st.error(t["error_company"].replace("{comp}", comp["name"]).replace("{err}", str(e)))
                progress_bar.progress((idx + 1) / total)

            duration = round(time.time() - start_time, 1)
            status_text.text("")
            
            st.session_state.batch_results = batch_results
            st.session_state.batch_duration = duration

    if st.session_state.batch_results is not None:
        duration = st.session_state.get("batch_duration", 0)
        st.success(t["success_batch"].replace("{time}", str(duration)))

        batch_results = st.session_state.batch_results
        if batch_results:
            # Prepare a summary dataframe for batch
            summary_data = []
            fields_keys = [
                "head_office_address",
                "representative_name",
                "representative_title",
                "capital",
                "established",
            ]
            for r in batch_results:
                row = {"Company": r.get("company")}
                for fk in fields_keys:
                    row[fk] = r.get(fk) or "-"
                summary_data.append(row)

            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary)

            # Export Buttons for Batch Results
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                csv_batch = pd.DataFrame(batch_results).to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Export All (CSV)",
                    data=csv_batch,
                    file_name="batch_results.csv",
                    mime="text/csv",
                )
            with col2:
                import json

                json_batch = json.dumps(batch_results, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 Export All (JSON)",
                    data=json_batch,
                    file_name="batch_results.json",
                    mime="application/json",
                )
