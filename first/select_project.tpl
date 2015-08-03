% show_help = "select_project"
% include('header.tpl')

<div style="margin-top: 3em;">
    <button value="Подать заявку" class="pure-button button" onclick="javascript:document.location='/request_access'">Подать заявку</button>

    <button class="pure-button button" onclick="javascript:document.location='/full_stats'">Статистика</button>

    <button value="Архив" class="pure-button button" onclick="javascript:document.location='/archive'">Архив</button>
</div>


<div style="display: {{'none' if len(projects) else 'block'}}">
    <h3>Добро пожаловать в Project Tracker!</h3>
    <p>Здесь панель управления вашими проектами.</p> 
    <p>Пока что у вас нет проектов.</p>
    <p>Это можно исправить путем отправки запроса на вступление в проект.</p>
</div>

<div style="display: {{'block' if len(projects) else 'none'}}">
<h3>Мои проекты:</h3>
<ul>
% for i in projects:
        <li><a href = "/projects/{{i.id}}"> {{i.name}} </a></li>
% end
</ul>
</div>


% include('footer.tpl', ver=ver, date=date)