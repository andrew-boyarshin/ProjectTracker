% include('header.tpl')

<!--suppress ALL -->
<h1> Проект : {{pr.name}} </h1>
<h3> Панель администратора </h3>

%if len (req):
    <div>
        <h4> Новые заявки: </h4>
        <table class="pure-table pure-table-bordered">
            <thead>
                <td> Принять заявку: </td>
                <td> Имя пользователя: </td>
                <td> Комментарий: </td>
            </thead>
            % for i in req:
                <p>
                    <tr>
                            <td>
                                <form action="/admin/{{pr.id}}/new_user" method="POST">
                                    <input type="submit" class="pure-button" name = "yes" value="Да">
                                    <input type="hidden" value ="{{i[1].id}}" name = "user_id">
                                    <input type="hidden" value ="{{i[0].id}}" name = "req_id">
                                    <input class="pure-button"  type="submit" name = "no" value="Нет">
                                    <input type="hidden" value ="{{i[0].id}}" name = "req_id">
                                </form>
                            </td>
                            <td>
                                {{i[1].name}}
                            </td>
                                <td>
                                    {{i[0].comment}}
                                </td>
                        </tr>
                </p>
            % end
        </table>
    </div>
% end

<div>
    <h4> Перевести проект на другой этап: </h4>
    <p style="display: {{'' if no_sow else 'none'}}">Невозможно перевести проект на следующий этап без ТЗ.</p>
    <form action="/admin/{{pr.id}}/change_stage" class="pure-form" method="POST">
        % for i in range (5):
        % text = ('Согласование ТЗ', 'Разработка', 'Приёмка', 'Сопровождение', 'Закрытие')[i]
            <input type="radio" name="stage" class="pure-radio" style="display: inline-block;" value="{{i+1}}"
            % if i + 1 == pr.stage:
            checked=""
            %end
            > {{text}} <br>
        % end
        <p> <input type="submit" class="pure-button" name = "change_stage" value="Применить"></p>
    </form>
</div>

<div>
<h4> Участники проекта: </h4>
<table class="pure-table pure-table-horizontal"> 
% for i in users:
    <p>
            <tr>
                <td>
                    <form class="pure-form" action="/admin/{{pr.id}}/del_user" method="POST">
                        <input type="submit" class="pure-button" name = "del_user" value="Выгнать">
                        <input type="hidden" value ="{{i[0].id}}" name = "uid">
                    </form>
                </td>
                <td>
                    {{i[0].name}}
                </td>
                 <td>
                    <form action="/admin/{{pr.id}}/change_user_role" class="pure-form" method="POST">
                        <select name = "new_role" class="pure-select" >
                        <option value = "{{i[1].id}}"> {{i[1].name}} </option>
                        % for j in cats:
                            % if j.id != i[1].id:
                                <option value = "{{j.id}}"> {{j.name}} </option>
                            % end
                        % end
                        </select>
                        <input type="submit" class="pure-button" name = "apply" value="Применить">
                        <input type="hidden" value ="{{i[0].id}}" name = "uid">
                    </form>
                </td>
            </tr>
    </p>
% end
</table>
</div>

<div>
    <h4> Создать категорию участников: </h4>

    <p style="display: {{'' if no_category else 'none'}}">Заполните все поля.</p>
    <form action="/admin/{{pr.id}}/create_usercat" class="pure-form" method="POST">
        <div class="pure-u-1-4">
            <!-- <div class="pure-g"> -->
                <!-- <div class="pure-u-1-5"> -->
                <!-- <p>Название: </p> -->
                <!-- <p>Права: </p> -->
                <!-- </div> -->
                <!-- <div class="pure-u-2-3"> -->
                <div class="pure-group">
                <input type = "text" class="pure-input" required name = "cat_name" style="width: 100%;">
                <!-- <input type = "text" class="pure-input" required name = "cat_rights" style="width: 100%;"> -->
                </div>
                <p><input type = "checkbox" class = "pure-input" name = "r_right" checked="" disabled=""> Чтение<br>
                <input type = "checkbox" class = "pure-input" name = "w_right"> Запись<br>
                <input type = "checkbox" class = "pure-input" name = "a_right"> Администрирование </p>
                <input type = "submit" class="pure-button" name = "create_cat" value="Создать" style=" margin-top: 1px; width: 100%;">
                <!-- </div> -->
                <!-- </div> -->
        </div>
    </form>
</div>

% include('footer.tpl', ver=ver, date=date) 