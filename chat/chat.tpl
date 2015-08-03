<div id="chat" style="padding: 0.5em;">
<center>
    <div style="background-color: #DDDDE5;">
        <b>Чат</b><br />
        
        </div>
        <a onclick="javascript:chat_history();" id="chat_history_link" style="
    text-decoration: none; padding: 5px 10px; color: #00E; font-size: 0.8em; line-height: 1.7em; white-space: normal;
">Загрузить больше сообщений</a>
    </center>
    <div id="chat-container">
    </div>
     <div class="write-container" >
        <div class="write-block" style="padding:0.5em;"> 
            <textarea id="chat-input" style="width: 100%;"
                      placeholder="Введите ваше сообщение. Поддерживается простое форматирование Markdown."></textarea>
        </div>
        <div class="send-block">
        <br>
            <button class="pure-button" id="chat-send-button" value="Отправить" onclick="javascript:chat_send();" title="Отправить ( Ctrl + Enter )" style="width:100%; background: rgb(170, 170, 200);">Отправить</button>
        </div>
    </div> 
</div>


<script type="text/javascript" src="/static/andrew/jquery-2.1.3.min.js"></script>
<script type="text/javascript" src="/static/chat/chat.js"></script>
<script type="text/javascript">
    setusername('{{cur_author}}')
    setpr_id('{{pr_id}}')
</script>