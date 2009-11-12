<%def name="extra_header_info()">
	<h2>${c.project.name}</h2>
	<div id="main-menu">
		<ul>
			<li class="selected"><a href="/projects/show/deluge" class="overview">Overview</a></li>
			<li><a href="/projects/activity/deluge" class="activity">Activity</a></li>
			<li><a href="/projects/settings/deluge" class="settings">Settings</a></li>
		</ul>
	</div>
</%def>
<%inherit file="base.mao" />
${next.body()}