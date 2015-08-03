% include('header.tpl')

<div class="container">
<div class="dash_settings">
    <div class="username">
        <h2>Cменить имя:</h2>
        <p style="display: {{'' if ch_name else 'none'}}">Имя успешно изменено.</p>
        <p style="display: {{'' if null_name else 'none'}}">Имя пользователя не может быть пустым.</p>
        <form action="/settings/save/username" class="pure-form" method="POST">
            <input type="text" class="pure-input" name="username" required="" value="{{username}}">
            <input type="submit" class="pure-button" value="Сохранить">
        </form>
    </div>
    <div class="password">
        <h2>Cменить пароль:</h2>

        <p style="display: {{'' if ch_pass else 'none'}}">Пароль успешно изменен.</p>
        <p style="display: {{'' if diff_new else 'none'}}">Введёные новые пароли не совпадают.</p>
        <p style="display: {{'' if wrong_pass else 'none'}}">Неверно введён текущий пароль.</p>
        <p style="display: {{'' if null_pass else 'none'}}">Поле пароля не может быть пустым.</p>
        <form action="/settings/save/password" class="pure-form" method="POST">
        <div class="pure-u-5-12">
            <div class="pure-g">
                <div class="pure-u-1-3">
                    <p>Текущий пароль:</p>
                    <p>Новый пароль:</p>
                    <p>Повторите пароль:</p>
                </div>
                <div class="pure-u-2-3">
                    <div class="pure-group">
                        <input type="password" class="pure-input" name="old" placeholder="Старый пароль" style="width: 100%;">
                        <input type="password" name="new" placeholder="Новый пароль" style="width: 100%;" class="pure-input">
                        <input class="pure-input" type="password" name="new_confirm" style="margin-top: -1px; width: 100%;" placeholder="Повторите пароль">
                        <input type="submit" class="pure-button" value="Сохранить" style="margin-top: 1px; width: 100%;">
                    </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>
</div>

% include('footer.tpl', ver=ver, date=date)