% not_show = True
% show_help = '0'
% include('header.tpl')
<div class="main_box">
    <div class="container">
        <div class="pure-g">
            <div class="pure-u-1-3"></div>
            <div class="pure-u-1-3">
                <center>
                    <form id="ourform" action="/login" class="pure-form" method="POST">
                        <p><font size="5px">
                        <img src="/static/icon.png" class="pure-img"/>
                        Project Tracker</font></p>
                        <font color="red">
                            <b>
                            <div style="display: {{'' if wrong else 'none'}}">Неправильный логин или пароль</div>
                            <div style="display: {{'' if already_reg else 'none'}}">Пользователь уже зарегистрирован</div>
                            <div style="display: {{'' if too_long else 'none'}}">Слишком длинный логин или пароль ( &gt; 20 символов )</div>
                            <div class="pure-group">
                            </b>
                        </font>
                        <!-- <center> -->
                            <input type="text" required="" class="pure-input" placeholder="Логин" name="nick"></input>
                            <input name="pass" required="" type="password" class="pure-input" placeholder="Пароль"></input>
                            <!-- </center> -->
                        </div>
                        <div class="pure-group">
                            <input onclick="javascript:register()" class="pure-button button-register"  type="button" value="Регистрация">  
                            <input onclick="javascript:login()" type="submit" class="pure-button button-login" value="Вход">
                        </div>
                    </form>
                </center>
            </div>
        </div>
    </div>

</div>

<script>
    function login() {
        form = document.getElementById("ourform");
        form.action = '/login';
        form.submit();
    }
    function register() {
        form = document.getElementById("ourform");
        form.action = '/register';
        form.submit();
    }
</script>



% include('footer.tpl', ver=ver, date=date)