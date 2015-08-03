% not_show = True
% include('header.tpl')

<div style="margin-top: 3em;">
    <h4>Cоздать проект:</h4>

    <div style="display: {{'' if exists else 'none'}}">Проект с таким именем уже существует</div>

    <form action="/sadm/create_project" class="pure-form" method="POST">
        <p>
            Имя проекта : <input class="pure-input" type="text" name="name" required>
            <input class="pure-button" type="submit" value="Создать">
        </p>
    </form>
</div>

<div>
<h4> Существующие проекты: </h4>

        <table class="pure-table pure-table-horizontal">
% for i in projects:
    <p>
            <tr>
                <td>
                    {{i.name}}
                </td>
                <td>
                    <form action="/sadm/{{i.id}}" class="pure-form" method="GET">
                        <input class="pure-button" type="submit" name = "edit" value="Редактировать">
                        <input class="pure-input" type="hidden" value ="{{i.id}}" name = "pr_id">
                    </form>
                </td>
                <td>
                    <form action="/sadm/delete_project" class="pure-form" method="POST">
                        <input class="pure-button" type="submit" name = "del" value="Удалить">
                        <input class="pure-input" type="hidden" value ="{{i.id}}" name = "pr_id">
                    </form>
                </td>
            </tr>
    </p>
% end

        </table>
</div>

<div>
<h4> Категории пользователей: </h4>
<table class="pure-table pure-table-bordered">
            <thead>
               <td>
                    Имя
               </td>
               <td>
                    Роль
               </td>
              <!--  <td>
                    Применить
               </td> -->
               <td>
                    Удалить
               </td> 
            </thead>
% for i in cats:
    <p>
            
            <tr>
                <!-- <td>
                    <form action="/sadm/change_cat" class="pure-form" method="POST">
                        <input class="pure-input" type = "edit" name = "cat_name" value = "{{i.name}}" required>   
                </td> -->
             <!--    <td>
                        <input class="pure-input" type = "edit" name = "cat_rights" value = "{{i.priv}}" required>
                </td>
                <td>
                        <input class="pure-button" type="submit" name = "apply" value="Применить">
                        <input class="pure-input" type="hidden" value ="{{i.id}}" name = "cid">
                    </form>
                </td> -->
                <td>
                    {{i.name}}
                </td>
                <td>
                % str = 'Читатель' 
                % if 'w' in i.priv:
                    % str += ', писатель'
                % end
                % if 'a' in i.priv:
                    % str += ', админ'
                % end
                {{str}}
                </td>
                 <td>
                    <form action="/sadm/del_cat" class="pure-form" method="POST">
                        <input class="pure-button" type="submit" name = "del_cat" value="Удалить">
                        <input class="pure-input" type="hidden" value ="{{i.id}}" name = "cid">
                    </form>
                </td>
            </tr>
        
    </p>
% end
</table>
</div>

% include('footer.tpl', ver=ver, date=date) 