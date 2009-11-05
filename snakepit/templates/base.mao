<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
	<head>
		<title>Snakepit</title>
		<link rel="stylesheet" href="/css/snakepit.css" type="text/css" />
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		
		<script src="/js/mootools-1.2.4-core-yc.js" type="text/javascript"></script>
		<script src="/js/snakepit.js" type="text/javascript"></script>
	</head>
	<body>
		<div id="container">
			<div id="toplinks">
				<div id="account">
					<ul>
						<li>
							<a class="login" href="/account/login">Sign in</a>
						</li>
						<li>
							<a class="register" href="/account/register">Register</a>
						</li>
					</ul>
				</div>
				<ul>
					<li>
						<a class="home" href="/">Home</a>
					</li>
					<li>
						<a class="proejcts" href="/projects">Projects</a>
					</li>
					<li>
						<a class="help" href="http://snakepit.damoxc.net/help">Help</a>
					</li>
				</ul>
			</div>
			<div id="header">
				% if c.project:
				<h1>${c.project.name}</h1>
				% else:
				<h1>Snakepit</h1>
				% endif
			</div>
			<div id="body">
				${next.body()}
			</div>
			<div id="footer">
				Powered by <a href="http://snakepit.damoxc.net">Snakepit</a> &copy; 2009 Damien Churchill
			</div>
		</div>
	</body>
</html>
