from flask import Flask, render_template, request
from summarizer import summarize_text
import os

app = Flask(__name__)

@app.route('/')
def index():
    """
    แสดงหน้าหลัก (index.html) ที่มีฟอร์มสำหรับกรอกข้อความ
    """
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    """
    รับข้อความจากฟอร์ม, เรียกใช้ฟังก์ชันสรุป, และแสดงผลลัพธ์
    """
    if request.method == 'POST':
        # ดึงข้อมูลจากฟอร์มที่ชื่อ 'text_to_summarize'
        original_text = request.form['text_to_summarize']

        # เรียกใช้ฟังก์ชันสรุปข้อความ
        summary = summarize_text(original_text)

        # ส่งผลลัพธ์กลับไปแสดงผลที่หน้าเดิม (index.html)
        return render_template('index.html', original_text=original_text, summary=summary)

if __name__ == '__main__':
    # ใช้ port ที่มาจาก environment variable หรือใช้ 5000 เป็นค่าดีฟอลต์
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)