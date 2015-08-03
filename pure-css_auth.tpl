<!DOCTYPE html>

<!-- author Ilya Gilyov, Igo Andrey, Ivanov Andrey
Date 30.07.2015
Ver 0.1 -->

<html>
<head>
	<meta charset="utf-8" />
	<title>Pure Test</title>
	<link rel="stylesheet" href="pure-css/pure-min.css">
	<style type="text/css">
		.pure-g div {
			text-align: center;
		}
		.pure-g .pure-u-1-2 {
			background-color: #FF7777;
		}
		.button-success,
		.button-error,
		.button-warning,
		.button-secondary,
		.button-nice {
		    background-color: transparent;
		}
		.button-success {
		    background: rgb(28, 184, 65); /* this is a green */
		}
		.button-error {
		    background: rgb(202, 60, 60); /* this is a maroon */
		}
		.button-login {
		    background-color: yellow;
		}
		.button-register {
		    background: rgb(66, 184, 221); /* this is a light blue */
		}
		#mymain {
			align: center;
		}
		.container {
			text-align: center;
		}
		.pure-g form div.pure-group input {
			width: 100%;
		}
	</style>
</head>
<body>
	<div class="container">
		<div class="pure-g">
			<div class="pure-u-1-3">
				<center>
				<form class="pure-form">
					
					<p><font size="5px">
					<img src="icon.png" class="pure-img" />
					Project Tracker</font></p>
					<div class="pure-group">
					<center>
						<input type="text" class="pure-input" placeholder="Логин"></input>
						<input type="password" class="pure-input" placeholder="Пароль"></input>
						</center>
					</div>
					<div class="pure-group">
					<input onclick="javascript:register()" class="pure-button button-register"  type="button" value="Регистрация">					
					<input onclick="javascript:login()" type="submit" class="pure-button button-login" value="Вход">
					</div>
				</form>
				</center>
			</div>
		</div>
	</div>

</body>
</html>