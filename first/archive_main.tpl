%for i in arh:
{{i.tickets}}
%end
% include('header.tpl')

<div style="display: {{'block' if len(arh) else 'none'}}">
<h3>Завершённые проекты:</h3>
<table class="pure-table pure-table-bordered" width="90%">
<thead>
 <td> Название </td>
 <td> Дата создания </td>
 <td> Дата закрытия </td>
 <td> Тикеты </td>
</thead>
% for i in arh:
			<tr>
				<td>
					<a href="/archive/{{i.id}}/stat">{{i.name}}</a>
				</td>
				<td>
					<nobr>{{i.create_time}}</nobr>
				</td>
				<td>
					<nobr>{{i.close_time}}</nobr>
				</td>
				<td width="40%">
					%tickets = i.tickets.split("/")
					%sum=int(tickets[3])
					%red = int(tickets[1]) - int(tickets[0])
					%yellow = sum-int(tickets[2])-red
					%green = int(tickets[2])
						%if sum != 0:
							%yellow_str = str((yellow*100)/sum) + "%"
							%green_str = str((green*100)/sum) + "%"
							%red_str = str((red*100)/sum) + "%"	
				<div class="pure-g">
% if red:
					<div class="nospace" style="padding:.5em 0em; background-color: red; width:{{red_str}};"></div>
% end
% if yellow:
					<div class="nospace" style="padding:.5em 0em; background-color: yellow; width:{{yellow_str}};"></div>
				
% end
% if green:
					<div class="nospace" style="background-color: green; padding:.5em 0em; width:{{green_str}};"></div>
% end
				</div>
					%else:
						 Нет
					%end

				</td>
			</tr>
% end
</table>
</div>

% include('footer.tpl', ver=ver, date=date)