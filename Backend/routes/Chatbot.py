from flask import render_template,redirect,session,Blueprint,jsonify,request,url_for
from Backend.services.Chroma import ask_question,store_chunks,serching_chunks
from Backend.models.videos import Video
from Backend.models.Conversation import Conversation
from Backend.models.Messages import Message
from Backend.extensions import db

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/chatbot/<int:video_id>', methods =['GET','POST'])
def chatbot(video_id):
    try:
        user_id =session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))  # Redirect to login if user is not logged in

        #varify this video_id is belong to this user or not
        videos = Video.query.filter_by(id= video_id, user_id = user_id).first()

        if not videos:
            return redirect(url_for('auth.login'))  # Redirect to login if user is not logged in

        #find the existing conversation for this user for this perticular video
        conversation = Conversation.query.filter_by(video_id = video_id , user_id = user_id).first()

        # Rule is simple 
        # 1 if user conversation is exists for this video then open that conversation 
        # 2 if user conversation is not exists for this video then create a new conversation and open that conversation
        if not conversation:
            conversation = Conversation(user_id = user_id,
                                        video_id = video_id,
                                        title = videos.title,
                                        )

            db.session.add(conversation)
            db.session.commit()
            

        if request.method == 'POST':
            question = request.form.get('question')
            

            message = Message.query.filter_by(conversation_id = conversation.id).order_by(Message.created_at.asc()).all()
            conversation_history = [
            {
                "role": i.role,
                "content": i.content    
            }
            for i in message
            ]
            
            # we stored new question asked by user in database for this conversation
            message = Message(conversation_id = conversation.id,
                              role = "user",
                                content = question
                                )
            db.session.add(message)
            db.session.commit()
            llm_response = ask_question(question, video_id, conversation_history=conversation_history)
            
            #storing the response of llm in database for this conversation
            message = Message(conversation_id = conversation.id,
                              role = "assistant",
                                content = llm_response
                                )
            db.session.add(message)
            db.session.commit()
            
            return llm_response

        
        return render_template("chatbot.html",video_id = video_id)
    
    except Exception as e :
        print("there is an error in chatbot route", e)
        return jsonify({"error" : str(e)})
    