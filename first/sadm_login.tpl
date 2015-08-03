% include('header.tpl')

<div class="main_box">
    <div class="container">
        <div class="pure-g">
            <div class="pure-u-1-3"></div>
            <div class="pure-u-1-3">
                <center>
                    <form id="ourform" action="/sadm" class="pure-form" method="POST">
                        <p><font size="5px">
                        <img src="/static/icon.png" class="pure-img"/>
                        Суперадминка</font></p>
                        <font color="red">
                            <b>
                            <div style="display: {{msg_viz}}">Неправильный логин или пароль</div>
                            <div class="pure-group">
                            </b>
                        </font>
                        <!-- <center> -->
                            <input type="text" required="" class="pure-input" placeholder="Логин" name="name"></input>
                            <input name="pass" required="" type="password" class="pure-input" placeholder="Пароль"></input>
                            <!-- </center> -->
                        </div>
                        <div class="pure-group">
                            <input type = "submit" value = "Войти" class="pure-button button-login">
                        </div>
                    </form>
                </center>
            </div>
        </div>
    </div>

</div>


<!-- 
<form action="/sadm" class="pure-form" method="POST">
<p style="display: {{msg_viz}}">Неправильный логин или пароль</p>
<p> Ник : <input class="pure-input" required="" type="text" name="name"></p>
<p> Пароль : <input class="pure-input" required="" type="password" name="pass"></p>
<input class="pure-button" type = "submit" value = "Login"> 
</form>
 -->
% include('footer.tpl', ver=ver, date=date)