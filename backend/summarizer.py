import os
import google.generativeai as genai
from dotenv import load_dotenv

# โหลดค่า API Key จากไฟล์ .env
load_dotenv()

# ตั้งค่า Gemini API
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')

except Exception as e:
    print(f"Error setting up Gemini API: {e}")
    model = None

def summarize_text(text_to_summarize):
    """
    ฟังก์ชันสำหรับสรุปข้อความโดยใช้ Gemini API
    """
    if not model:
        return "Error: Gemini model is not available. Please check API key configuration."

    try:
        # สร้าง prompt สำหรับการสรุปข้อความ
        prompt = f"Please summarize the following text in a concise way:\n\n{text_to_summarize}"

        # ส่ง prompt ไปยัง Gemini
        response = model.generate_content(prompt)

        # ดึงข้อความที่สรุปแล้วออกมา
        summary = response.text
        return summary

    except Exception as e:
        return f"An error occurred during summarization: {e}"

if __name__ == '__main__':
    # ตัวอย่างการใช้งาน
    sample_text = """
    Python is an interpreted, high-level and general-purpose programming language.
    Python's design philosophy emphasizes code readability with its notable use of
    significant whitespace. Its language constructs and object-oriented approach
    aim to help programmers write clear, logical code for small and large-scale projects.
    Python is dynamically-typed and garbage-collected. It supports multiple programming
    paradigms, including structured (particularly, procedural), object-oriented,
    and functional programming. Python is often described as a 'batteries included'
    language due to its comprehensive standard library.
    """
    print("--- Original Text ---")
    print(sample_text)
    print("\n--- Summary ---")
    summary_result = summarize_text(sample_text)
    print(summary_result)