% include('header.tpl')

<h1 align = "center"> Проект "{{pr.name}}" завершён</h1>

<p align = "center" valign = "center">
<!-- <a><img src = "/static/ok.png"></a> -->
<font color="#66FF66" size="20em"><i class="fa fa-check fa-5x"></i></font>
</p>

<p align = "center" valign = "center">
<b> cong & grats </b> <br>
<a href="/archive/{{pr.id}}/stat"> Cтатистика </a>
</p>
% include('footer.tpl', ver=ver, date=date)