<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>WS10: Project Tracker</title>
    <link type="text/css" href="/static/andrew/simplest.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/pure-css/pure-min.css">
    <link rel="stylesheet" href="/static/pure-css/font-awesome-4.2.0/css/font-awesome.css">
	<style type="text/css">
        body {
            font-family: 'Verdana', sans-serif;
        }
		.button-success,
		.button-error,
		.button-warning,
		.button-secondary,
		.button-nice {
		    background-color: transparent;
		}
		.button-success {
		    background: rgb(40, 220, 70); /* this is a green */
		}
		.button-error {
		    background: rgb(240, 150, 30); /* this is a maroon */
		}
		.button-login {
		    background-color: yellow;
		}
		.button-register {
		    background: rgb(66, 184, 221); /* this is a light blue */
		}
		.pure-g form div.pure-group input {
			width: 100%;
		}
        a {
            text-decoration: none;
            padding: 5px 10px;
            /*color: #555;*/
            font-size: 1.2em; 
            line-height: 1.7em; 
            white-space: nowrap;
        }
        .pure-menu li a {
            padding: 5px 0.5em;
        }
	</style>
</head>
<body>


<header>
<div class="pure-menu pure-menu-open pure-menu-horizontal pure-menu-fixed">
    <a class="pure-menu-heading" style="line-height: 2em;">WS10: Project Tracker</a>
    <ul style="float: right;">
        <li class="pure-menu-selected"><a href="/"><i class="fa fa-home"></i> На Главную</a></li>
% if "show_help" in globals():
        <li class="pure-menu-selected"><a href="/help/{{show_help}}"><i class="fa fa-question-circle"></i>  Справка</a></li>
% end

%if not "not_show" in globals():
        <li class="pure-menu-selected"><a href="/settings"><i class="fa fa-gear"></i> Настройки</a></li>
		<li class="pure-menu-selected"><a href="/logout"><i class="fa fa-close"></i> Выход</a></li>
% end
    </ul>
</div>
</header>


<div class="header-margin"></div>

% if 'pr_id' in dir():
<div class="pure-g">
<div class="pure-u-3-4">
% end