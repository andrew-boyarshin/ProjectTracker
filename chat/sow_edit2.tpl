% show_help = 1
% include('header.tpl', pr_id=pr_id, cur_author=cur_author)

% if show:
<table align = "left" valign = "top" width="100%">
<tr align = "left" valign = "top">
<td align = "left" valign = "top">
<p style="display: {{'' if null_sow else 'none'}}">Введите хотя бы один заголовок первого уровня.</p>

 <form action="/projects/{{pr_id}}/edit_sow_apply" method="POST">
   <p> <input type="submit" name = "apply" value="Применить"> </p>
    <textarea id = "sow" name ="sow" rows="20" columns="20" placeholder="Техническое задание в формате Markdown">{{md}}</textarea>
</form>



</td>


% if esow:
<td align = "left" valign = "top">
 <form action="/projects/{{pr_id}}/sow_approve" method="POST">
   <p> <input type="submit" name = "apply" value="
    % if not my_app:
        Проголосовать за вариант
    % else:
        Отозвать свой голос
    % end
    "> </p>
    <input type = "hidden" name = "type" value = "
    % if not my_app:
        app
    % else:
        del
    % end
    "></input>
% end
       {{html}}
% end
% if show:
</form>
</td>
</tr>
</table>
% end

% if esow:
% for i in users:
<p> {{i[0].name}}

% if i[1]:
    - OK
% else:
    - Not OK
% end

</p>

% end
% end

% if not show and not esow:

<p>
Техническое задание ещё не создано.<br>
У вас нет прав на его создание и редактирование.
</p>

% end

% if show and esow:

<select id = "sow_ver" onchange = "javascript:get_backup({{pr_id}});">

% for i in sows:

    <option value = "{{i[0].id}}"> {{i[1].name}} ({{i[0].edit_time}}) </option>

% end

</select>

<script type="text/javascript" src="/static/andrew/jquery-2.1.3.min.js"></script>

<script>
function get_backup(pr_id){
    var ch = document.getElementById("sow_ver").value;
    $.getJSON ("/projects/"+pr_id+"/sow/get_backup?sowid="+ch, function (json){
        var text = document.getElementById ("sow");
        text.innerHTML = json.md;
        // alert (12);
    })
}
</script>

% end

% include('footer.tpl', ver=ver, date=date, pr_id=pr_id, cur_author=cur_author)