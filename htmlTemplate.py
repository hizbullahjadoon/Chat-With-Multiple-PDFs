# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 18:42:09 2024

@author: Hizbullah
"""

css = '''
<style>
.chat-container {
    display: flex;
    flex-direction: column-reverse;
}

.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 15%;
}
.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 85%;
    padding: 0 1.5rem;
    color: #ffff;
}
</style>

'''

bot_template = '''
<div class="chat-container">
<div class="chat-message bot">
    <div class="avatar">
        <img src="C:/Users/Hizbullah/Documents/FILES/Spyder/Project 1/DSC_0033">
    </div>
    <div class="message">{{MSG}}</div> 
</div>
</div>
'''

user_template = '''
<div class="chat-container">
<div class="chat-message user">
    <div class="avatar">
        <img src="C:/Users/Hizbullah/Documents/FILES/Spyder/Project 1/DSC_00331">
    </div>
    <div class="message">{{MSG}}</div>
</div>
</div>
'''
