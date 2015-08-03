% include('header.tpl', pr_id=pr_id, cur_author=cur_author)

<div class="pure-g">
    <div class="pure-u-1-2">
        % if not show and not esow:
        <p style="color: red;">
        <b>Техническое задание ещё не создано.<br>
        У вас нет прав на его создание и редактирование.</b>
        </p>
        %end
    % if show:
        <p style="display: {{'' if null_sow else 'none'}}; color: red;"><b>Введите хотя бы один заголовок первого уровня.</b></p>
        <form action="/projects/{{pr_id}}/edit_sow_apply" method="POST" class="pure-form">
            <textarea id = "sow" class="pure-input" name ="sow" rows="20" columns="20" placeholder="Техническое задание в формате Markdown">{{md}}</textarea>
            <p> <input type="submit" class="pure-button" name = "apply" value="Применить"> </p>
        </form>
        <div style="background-color: #EEEEEE;">
            <h4>Справка</h4>
            MarkDown для чайников
        </div>
        % end
    </div>
    <div class="pure-u-1-2">
    % if esow:
    <!-- <td align = "left" valign = "top"> -->
        <form action="/projects/{{pr_id}}/sow_approve" method="POST">
        <input type="submit" class="pure-button" name = "apply" value="
        % if not my_app:
            Проголосовать за вариант
        % else:
            Отозвать свой голос
        % end
        ">
        <input type = "hidden" name = "type" value = "
        % if not my_app:
            app
        % else:
            del
        % end
        "></input>
    % end
    {{html}}
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
    </div>
</div>

%end

%include('footer.tpl', ver=ver, date=date, pr_id=pr_id, cur_author=cur_author) 
