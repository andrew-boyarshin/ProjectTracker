% include('header.tpl')
	<h1>Статистика</h1>
	<h3>Проекты</h3>
	<table width="100%" class="pure-table pure-table-bordered" border="2" cellspacing="0" cellpadding="3">
		<thead>
			<td width="150px">
				Имя
			</td>
			<td width="200px">
				Время создания
			</td>
			<td width="120px">
				Этап			
			</td>
			<td>
				Тикеты
			</td>
		</thead> <!--<img src="green.gif" width=300px height=20px>		-->
				%for i in projects:
			<tr>
			<!-- <br> {{i.id}} <br> -->
				<td>
					{{i.name}}
				</td>
				<td>
					{{i.create_time}}
				</td>
				<td>
					{{i.stage}}
				</td>		
					%red = yellow = green = mysum = 0
					%for j in tickets:
						<!-- Project - {{i.id}} -->
						%if j.pid == i.id:
							%if j.closed:
								%green+= 1	
							%elif j.category == 3 or j.category == 4:
								%red+= 1
							%else:
								%yellow+= 1
							%end	
							%mysum+= 1
						%end
					%end	

				<td>
						%if mysum == 0:
							Нет
						%else:
							%yellow_str = str((yellow*100)/mysum) + "%"
							%green_str = str((green*100)/mysum) + "%"
							%red_str = str((red*100)/mysum) + "%"
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
			</tr>

				%end
			%end
		</td>
	</table>

<style type="text/css">
.nospace {
	display: inline-block;
	zoom: 1;
	letter-spacing: normal;
	word-spacing: normal;
	vertical-align: top;
	text-rendering: auto;
}
</style>

% include('footer.tpl', ver=ver, date=date)