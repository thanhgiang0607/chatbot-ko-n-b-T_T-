from flask import Flask, render_template, request, jsonify
import openai
from openai import OpenAI

# Khởi tạo OpenAI client
client = OpenAI(api_key="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")
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("chatbot.html")

@app.route("/ask", methods=["POST"])
def ask():
    print("\n=== DEBUG: /ask route được gọi ===")
    
    try:
        # Debug: Kiểm tra request
        print(f"Request method: {request.method}")
        print(f"Request content type: {request.content_type}")
        print(f"Request data: {request.get_data()}")
        
        # Lấy message từ request
        if not request.json:
            print("ERROR: No JSON data in request")
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_input = request.json.get("message")
        print(f"User input: {user_input}")
        
        if not user_input:
            print("ERROR: No message in JSON")
            return jsonify({"error": "No message provided"}), 400
        
        print("Đang gọi OpenAI API...")
        
        # Gọi OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        
        print("OpenAI API response nhận được!")
        
        # Truy cập đúng cách với OpenAI client mới
        reply = response.choices[0].message.content
        print(f"Reply: {reply}")
        
        return jsonify({"reply": reply})
        
    except Exception as e:
        print(f"Lỗi trong /ask route: {e}")
        print(f"Loại lỗi: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)