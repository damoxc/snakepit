<%def name="extra_header_info()">
	<h2>${c.project.name}</h2>
	<div id="main-menu">
		<ul>
			% for menu_item in c.menu_items:
			<%url = menu_item.get_url(c.project.identifier)%>
			% if c.url.startswith(url):
				<li class="selected">
			% else:
				<li>
			% endif
					% if menu_item.class_:
					<a href="${url}" class="${ menu_item.class_}">${menu_item.label}</a>
					% else:
					<a href="${url}">${menu_item.label}</a>
					% endif
				</li>
			% endfor
		</ul>
	</div>
</%def>
<%inherit file="base.mao" />
${next.body()}