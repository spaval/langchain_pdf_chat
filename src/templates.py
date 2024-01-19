css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 24px;
  max-height: 24px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://firebasestorage.googleapis.com/v0/b/bongga-248c4.appspot.com/o/assets%2Fimages%2Fbot.png?alt=media&token=777401a1-9286-41ee-ab97-c757824d07a5" alt='Bot' />
    </div>
    <div class="message">{{message}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://firebasestorage.googleapis.com/v0/b/bongga-248c4.appspot.com/o/assets%2Fimages%2Fuser.png?alt=media&token=e080e6c3-10ae-450c-ab17-23d00b671bef" alt='User' />
    </div>    
    <div class="message">{{message}}</div>
</div>
'''