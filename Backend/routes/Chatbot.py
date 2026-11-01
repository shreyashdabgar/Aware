from flask import render_template,redirect,session,Blueprint,jsonify,request
from Backend.services.Chroma import ask_question,store_chunks,serching_chunks


chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/chatbot/<int:video_id>', methods =['GET','POST'])
def chatbot(video_id):
    try:
        if request.method == 'POST':
            question = request.form.get('question')
            
            llm_response = ask_question(question, video_id)

            return llm_response

        
        return render_template("chatbot.html",video_id = video_id)
    
    except Exception as e :
        print("there is an error in chatbot route", e)
        return jsonify({"error" : str(e)})
    