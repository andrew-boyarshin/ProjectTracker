% show_help = '1'
% include('header.tpl', pr_id=pr_id, cur_author=cur_author)
<div class="pure-g sow-edit-table">
    % if not show and not esow:
        <div class="pure-u-1">
            <p style="color: red;">
                <b>
                    Техническое задание ещё не создано.<br>
                У вас нет прав на его создание и редактирование.
                </b>
            </p>
        </div>
    %end
    % if show:
        <div class="pure-u-11-24 pure-form">
            %if esow:
                 <select id = "sow_ver" class="pure-input" onchange = "javascript:get_backup({{pr_id}});">
                % for i in sows:
                    <option value = "{{i[0].id}}"> {{i[1].name}} ({{i[0].edit_time}}) </option>
                % end
                </select>
            %end
            <p style="display: {{'' if null_sow else 'none'}}; color: red;"><b>Введите хотя бы один заголовок первого уровня.</b></p>
            <div class="pure-form">
                <pre id = "sow" class="pure-input" placeholder="Техническое задание в формате Markdown">{{md}}</pre>
                <div style="background-color: #EEEEEE;">
                    <h4>Справка</h4>
                    =======  раздел <br>
                    -------  подраздел <br>
                    ### заголовок <br>
                    **полужирный текст** <br>
                    __полужирный текст__ <br>
                    *текст курсивом* <br>
                    _текст курсивом_ <br>
                    * ненумерованный список <br>
                    1. нумерованный список
                </div>
            </div>
        </div>
    % end
    <div class="pure-u-1-24" style="width: 1.6667%"></div>
    % if show or esow:
        <div class="pure-u-11-24" style="word-break: break-word;">
            <div align="center">
                %if show:
                    <span>
                        <button id="save_sow" class="pure-button" value="Применить">
                            <i class='fa fa-save'></i> Применить
                        </button>
                        % if esow:
                            <form id="sow_approve_form" action="/projects/{{pr_id}}/sow_approve" method="POST"
                                  style="display: inline-block;">
                                <button class="pure-button" id="sow_approve_button" name = "apply" value="
                                        % if not my_app:
                                            Проголосовать
                                        % else:
                                            Отозвать голос
                                        % end
                                    "><i class='fa
                                        % if not my_app:
                                            fa-check
                                        % else:
                                            fa-close
                                        % end
                                    '></i>
                                    % if not my_app:
                                        Проголосовать
                                    % else:
                                        Отозвать голос
                                    % end
                                </button>
                                <input type = "hidden" name = "type" value = "
                                    % if not my_app:
                                        app
                                    % else:
                                        del
                                    % end
                                ">
                            </form>
                        % end
                    </span>
                % end
            </div>
            % if esow:
                {{html}}
                <center style="background-color: #DDDDE5;">
                    <h3>Голоса пользователей:</h3>
                </center>
                <table class="pure-table pure-table-horizontal">
                    % for i in users:
                        <tr>
                            <td>
                                % if i[1]:
                                    <i class="fa fa-check" title="OK"></i>
                                % else:
                                    <i class="fa fa-close" title="Not OK"></i>
                                % end
                            </td>
                            <td>{{i[0].name}}</td>
                        </tr>
                        % end
                </table>
            % end
        </div>
    % end
</div>
%end

<script type="text/javascript" src="/static/andrew/jquery-2.1.3.min.js"></script>
<script src="/static/ace/ace.js" type="text/javascript" charset="utf-8"></script>

<script>
function ready(fn) {
    if (document.readyState != 'loading'){
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}
function get_backup(pr_id){
    var ch = document.getElementById("sow_ver").value;
    $.getJSON ("/projects/"+pr_id+"/sow/get_backup?sowid="+ch, function (json){
        var text = document.getElementById ("sow");
        text.innerHTML = json.md;
        // alert (12);
    })
}
var aedit;
function onloadinit() {

    var b = document.getElementById('save_sow');
    if (b) {
        b.onclick = function () {
            $.post('http://localhost:8080/projects/{{pr_id}}/edit_sow_apply', {sow: aedit.getValue()}, function(res) {
                document.location = document.location;
            });
        };
    }
    var ab = document.getElementById('sow_approve_button');
    if (ab) {
        ab.onclick = function () {
            document.getElementById('sow_approve_form').submit()
        };
    }

    if (document.getElementById('sow')) {
        aedit = ace.edit('sow');

        aedit.setTheme('ace/theme/dreamweaver');
        aedit.getSession().setMode('ace/mode/markdown');
        aedit.setFontSize('16px');
    }
}
ready(onloadinit);
</script>

<style>
    pre#sow {
        height: {{max(md.count('\n')+2, 25)}}em;
        min-height: 30%;
        max-height: 50%;
    }
</style>

%include('footer.tpl', ver=ver, date=date, pr_id=pr_id, cur_author=cur_author) 