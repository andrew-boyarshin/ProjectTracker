ticket_inputs = {}

function len(o) {
    var res = 0;
    for (x in o) {
        res++;
    }
    return res;
}

function load_data(project_id, header_id, ignore_close) {
    parent = document.getElementById('parent-'+header_id);
    if ((parent.dataset['opened'] == 'true') && (ignore_close !== true)) {
        parent.dataset['opened'] = 'false';
        for (var i=0; i<parent.children.length; i++) {
            var item = parent.children[i];
            if (item.tagName != 'H2') {
                parent.removeChild(item);
                --i;
            }
        }
    } else {
        $.getJSON('/projects/'+project_id+'/dev/load/' + header_id, function(json) {
            var readonly = json.ro==='True';
            md = document.createElement('p');
            md.innerHTML = json.html;
            ul = document.createElement('ul');
            ul.classList.add('ticket-list')
            for (var i=0; i<json.tickets.length; i++) {
                var ticket = json.tickets[i];
                var li = document.createElement('li');
                var pure_g = document.createElement('div');
                pure_g.classList.add('pure-g');
                pure_g.classList.add('ticket-header');
                var h3 = document.createElement('h3');
                h3.classList.add('pure-u-3-4');
                h3.innerHTML = ticket.name;
                var span = document.createElement('span');
                span.classList.add('pure-u-1-4');
                span.classList.add('right-ticket-span');
                span.classList.add('pure-form');
                {
                    var crit = document.createElement('span');
                    crit.innerHTML = "Критично!";
                    crit.id = 'critical-span-'+ticket.id
                    crit.classList.add('crit-span');
                    crit.style.display = ((ticket.category == 3) || (ticket.category == 4))?'':'none';
                    span.appendChild(crit);
                }
                {
                    var wts = document.createElement('span');
                    var sel = document.createElement('span');
                    var matches = {1: 'I', 2: 'W', 3: 'E', 4: 'F', 5: 'R'};
                    sel.innerHTML = matches[ticket.category];
                    sel.classList.add('ticket-cat-select-plain');
                    sel.dataset['ticket_id'] = ticket.id
                    var matches_tooltip = {1: 'Информационный тикет', 2: 'Предупреждение',
                        3: 'Сообщение об ошибке', 4: 'Фатальная ошибка', 5: 'Запрос функционала'};
                    var notice_to_stupid_users = ". Нажмите чтобы изменить.";
                    sel.title = matches_tooltip[ticket.category] + notice_to_stupid_users;
                    if (!readonly)
                    {
                        sel.onclick = function (event) {
                            var parent = event.currentTarget.parentElement;
                            event.currentTarget.style.display = 'none';
                            var sel = document.createElement('select');
                            sel.classList.add('pure-input');
                            var invertedMatches = {'I': 1, 'W': 2, 'E': 3, 'F': 4, 'R': 5};
                            var neededText = invertedMatches[event.currentTarget.innerHTML];
                            for (var j=1; j<=5; j++) {
                                var opt = document.createElement('option');
                                opt.value = j;
                                opt.innerHTML = matches[j];
                                if (neededText === j) {
                                    opt.selected = true;
                                }
                                sel.appendChild(opt);
                            }
                            sel.dataset['ticket_id'] = event.currentTarget.dataset['ticket_id'];
                            sel.onchange = function (event) {
                                for (var j=0; j<5; j++) {
                                    var opt = event.target[j];
                                    if (opt.selected === true) {
                                        var tick_id = event.currentTarget.dataset['ticket_id'];
                                        $.post('/projects/'+project_id+'/dev/ticket/'+tick_id+'/set_category', {val: j+1},
                                            function(received_data) {
                                                var prevSpan = event.target.previousElementSibling;
                                                prevSpan.style.display = '';
                                                prevSpan.innerHTML = matches[j+1];
                                                prevSpan.title = matches_tooltip[j+1] + notice_to_stupid_users;
                                                event.target.parentElement.removeChild(event.target);
                                                {
                                                    var crit = document.getElementById('critical-span-'+tick_id);
                                                    crit.style.display = ((j == 2) || (j == 3))?'':'none';
                                                }
                                        });
                                        break;
                                    }
                                }
                            };
                            parent.insertBefore(sel);
                        };
                    }
                    wts.appendChild(sel);
                    span.appendChild(wts);
                }
                {
                    var check = document.createElement('input');
                    check.type = "checkbox";
                    check.placeholder = "Отметка, выполнен ли тикет";
                    check.checked = (ticket.closed === "true") || (ticket.closed === true)
                    check.dataset['ticket_id'] = ticket.id
                    if (readonly)
                    {
                        check.disabled = "true"    
                    } 
                    else 
                    {
                    check.onchange = function (event) {
                        $.ajax({
                            url: '/projects/'+project_id+'/dev/'+event.target.dataset['ticket_id']
                                +'/'+(event.target.checked?'':'un')+'mark',
                            success: function() {}
                        });
                    };
                    }
                    span.appendChild(check);
                }
                pure_g.appendChild(h3);
                pure_g.appendChild(span);
                li.appendChild(pure_g);
                var p = document.createElement('p');
                p.innerHTML = ticket.content;
                li.appendChild(p);
                var cd = document.createElement('div');
                cd.classList.add('comments-container');
                ticket.comments.forEach(function(item, j){
                    var d = document.createElement('div');
                    var p = document.createElement('p');
                    p.innerHTML = item.msg;
                    d.appendChild(p);
                    var date_p = document.createElement('p');
                    ed = ''
                    if (item.edit_time) {
                        ed = ' и отредактировал(а) ' + item.edit_time
                    }
                    date_p.innerHTML = '<b>' + item.nick + '</b> написал(а) ' + item.add_time + ed
                    d.appendChild(date_p);
                    cd.appendChild(d);
                });
                if (!readonly)
                {
                    var d = document.createElement('div');
                    d.classList.add('pure-form');
                    var texta = document.createElement('textarea');
                    texta.classList.add('pure-input');
                    texta.placeholder = "Введите комментарий и нажмите Ctrl+Enter"
                    texta.dataset['ticket_id'] = ticket.id
                    $(texta).keypress(function(data) {
                        if ((data.ctrlKey === true) && ((data.charCode === 10) || (data.charCode === 13))) {
                            data.preventDefault();
                            $.post('/projects/'+project_id+'/dev/ticket/'+data.target.dataset['ticket_id']+'/comment_create', {msg: data.target.value}, function(received_data) {
                                var old_count = parent.children.length;
                                load_data(project_id, header_id, true);
                                for (var i=1; i<=old_count; i++) {
                                    if (parent.children.length > 1) {
                                        parent.removeChild(parent.children[1]);
                                    }
                                }
                            })
                        }
                    })
                    d.appendChild(texta);
                    cd.appendChild(d);
                }
                li.appendChild(cd);
                ul.appendChild(li);
            }
            if (!readonly)
            {
                var li = document.createElement('li');
                li.classList.add('pure-form');
                var h3 = document.createElement('h3');
                h3.innerHTML = 'Cоздать новый тикет';
                li.appendChild(h3);
                var in_ticket = document.createElement('textarea');
                {
                    in_ticket.classList.add('pure-input');
                    in_ticket.placeholder = 'Введите текст тикета и нажмите Ctrl+Enter'
                }
                li.dataset['ti_i'] = len(ticket_inputs);
                ticket_inputs[li.dataset['ti_i']] = in_ticket;
                li.dataset['editing_now'] = "false";
                li.onclick = function(event) {
                    if (event.currentTarget.dataset['editing_now'] === "false") {
                        event.currentTarget.removeChild(event.currentTarget.children[0]);
                        event.currentTarget.appendChild(ticket_inputs[event.currentTarget.dataset['ti_i']]);
                        event.currentTarget.dataset['editing_now'] = true;
                    }
                };
                $(in_ticket).keypress(function(data) {
                    if ((data.ctrlKey === true) && ((data.charCode === 10) || (data.charCode === 13))) {
                        data.preventDefault();
                        $.post('/projects/'+project_id+'/dev/'+header_id+'/ticket_create', {data: data.target.value}, function(received_data) {
                            data.target.parentElement.removeChild(data.target);
                            $(data.target).keypress(undefined);
                            var old_count = parent.children.length;
                            load_data(project_id, header_id, true);
                            for (var i=1; i<=old_count; i++) {
                                if (parent.children.length > 1) {
                                    parent.removeChild(parent.children[1]);
                                }
                            }
                        })
                    }
                })
                ul.appendChild(li);
            }
            parent.appendChild(md);
            parent.appendChild(ul);
            parent.dataset['opened'] = 'true';
        });
    }
}