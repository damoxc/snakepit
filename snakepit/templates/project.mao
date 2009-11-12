<%def name="extra_header_info()">
	<h2>${c.project.name}</h2>
	<div id="main-menu">
		<ul>
			% for menu_item in c.menu_items:
			<%url = menu_item.get_url(c.project.identifier)%>
			% if url == c.url:
				<li class="selected">
			% else:
				<li>
			% endif
					<a href="${url}">${menu_item.label}</a>
				</li>
			% endfor
			<li class="selected"><a href="/projects/show/deluge" class="overview">Overview</a></li>
			<li><a href="/projects/activity/deluge" class="activity">Activity</a></li>
			<li><a href="/projects/settings/deluge" class="settings">Settings</a></li>
		</ul>
	</div>
</%def>
<%inherit file="base.mao" />
${next.body()}