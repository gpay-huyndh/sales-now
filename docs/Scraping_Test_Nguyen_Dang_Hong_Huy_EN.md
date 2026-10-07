**Please translate this requirement from Japanese and answer it.**

# **【Web Scraping and Data Extraction Assignment】**

## **1. Overview**

This test is a practical examination designed to evaluate your practical data collection abilities, your thought process in technology selection, and your skills in effectively utilizing Generative AI. Please submit your work using the specified method within 9 hours from the start time. You will be evaluated based on the commit contents at the specified time. Even if you do not complete it within the time limit, the process of your approach will be evaluated, so please commit whatever parts you have finished by the deadline.

## **2. Assignment A: Data Extraction from Company Websites**

Using the URL list of the following 10 listed companies as input data, scrape the official websites of each company by following the links, and use Generative AI to extract the specified data. Since the design and structure of each site are different, ensure your solution has a high degree of versatility. Write the setup instructions and execution methods for your created environment in Japanese in the `README.md` file.

* **Target Sites:**

| Company Name | URL |
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

* **Data to Extract:** Head office address, Representative's name, Capital, Date of establishment (Year and Month)

## **3. Assignment B: Challenge Against Bot Protection Sites 【Bonus / Optional】**

(Only for those who have fully completed Assignment A) Try extracting data from sites that block standard scraping methods.

* **Target Page:** [https://vn.indeed.com/jobs?q=remote](https://vn.indeed.com/jobs?q=remote)
* **Report Contents (to be documented in `report.md`):**
  * What kind of Bot countermeasures are being implemented?
  * What approaches did you try to counter them, and what were the results?

## **4. Technology Selection and Approach Comparison**

When acquiring data, evaluate and compare multiple methods (various libraries, frameworks, no-code tools, use of Generative AI APIs, etc.).
  Example: Python + Playwright + LangChain, TypeScript + Firecrawl + Vercel AI SDK, Dify, n8n.
When comparing, focus on the following three axes for evaluation, and write your reasons for selection in `report.md`.

* **Cost:** Development time, infrastructure expenses, tool usage fees, etc.
* **Speed:** Development speed and execution speed of data acquisition.
* **Quality / Completeness:** Accuracy of the data and minimization of omissions.

## **5. Usage of Generative AI**

For this assignment, **you are free to use Generative AI** such as ChatGPT, Claude, GitHub Copilot, etc.
However, you must comply with the following condition:
⚠️ **Mandatory Condition:** If you use chat-based AI like ChatGPT or Claude, please submit the history of your prompts and responses (or a shared link).

## **6. Submission Method**

All deliverables must be submitted via **GitHub**.

1. **Repository Creation:** Please create a private repository.
2. **Granting Access:** Invite the following two specified GitHub IDs from our company as collaborators:
   * atsunori0406
   * salesnow-tomohiro
3. **Directory Structure (Recommended):** Organize your repository as follows:
   `├── prompts/      # History of prompts used for Generative AI (txt format)`
   `├── result/       # Acquired data (CSV or JSON format)`
   `├── src/          # Source code you actually created`
   `├── README.md     # Setup and execution manual`
   `└── report.md     # Technology selection comparison chart and Assignment B insights`

## **7. Evaluation Criteria**

* **Understanding:** Have you correctly understood the essence of the assignment?
* **Design Ability:** Have you made appropriate technology selections considering cost, speed, and quality?
* **AI Utilization:** Have you effectively mastered Generative AI and built an appropriate flow?
* **Documentation:** Can you write documentation that is easily understandable by a third party?
