<%def name="extra_header_info()"></%def>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
	<head>
		<title>Snakepit</title>
		${h.tags.stylesheet_link('/css/snakepit.css')}
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		
		${h.tags.javascript_link('/js/mootools-1.2.4-core-yc.js', '/js/snakepit.js')}
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
						<a class="projects" href="/projects">Projects</a>
					</li>
					<li>
						<a class="help" href="http://snakepit.damoxc.net/help">Help</a>
					</li>
				</ul>
				<br style="clear: both;" />
			</div>
			<div id="header">
				<h1><span>Snakepit</span></h1>
				<%self:extra_header_info />
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
