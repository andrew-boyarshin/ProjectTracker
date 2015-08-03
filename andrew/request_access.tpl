% include('header.tpl')
<div class="container">

% from common import rus_declension

% if len (res_already):

<div>
    Мои заявки:
</div>
<ul id="already_requested">
<table class = "pure-table pure-table-horizontal">
% for i in res_already:
        <tr>
        <td>
        <span>{{i[0].name}}</span>
        </td>
        <td>
        <button class = "pure-button" onclick="document.location='/request/cancel/{{i[1].id}}'" value="Отмена">Отмена</button>
        </td>
        </tr>
% end

    </table>
</ul>
% end

% if len (res_avail):

<div>
    Присоединиться к проекту:
</div>
<ul id="available">
<table class = "pure-table pure-table-horizontal">
% for i in res_avail:
        <tr>
        <td>
        <span>{{i[0].name}}</span>
        </td>
        <td>
            ({{i[1]}} {{rus_declension (i[1], ('участник', 'участника', 'участников'))}})
        </td>
        <td>
        <button class = "pure-button" onclick="javascript:apply({{i[0].id}})" value="Запрос">Запрос</button>
        <form class="pure-form">
        <div style="display:none" id="comment-{{i[0].id}}-parent">
                    Введите комментарий и нажмите <br>
            "Запрос" еще раз для отправки запроса.<br>
                <input type="text" class ="pure-input" id="comment-{{i[0].id}}" placeholder="Ваш комментарий (рекомендуется)" style="width: 100%">
        </div>
        </form>
        </td>
        </tr>
% end
</table>
</ul>
</div>


<script>
    data = {}
    function apply(id) {
        field = document.getElementById("comment-"+id);
        field_block = document.getElementById("comment-"+id+"-parent");
        if (data[id] !== undefined) {
            document.location="/request/apply/" + id + "/"+field.value;
            data[id] = undefined;
            field_block.style.display = 'none';
        } else {
            data[id] = true;
            field_block.style.display = 'block';
        }
    }
</script>

% else:

<div>
Нет проектов, доступных для присоединения.
</div>

% include('footer.tpl', ver=ver, date=date)