<%inherit file="/project.mao" />
<h2>Settings</h2>
<div class="tabs">
	<ul>
		% for name, title in c.tabs:
		<li><a href="${h.url_for(tab=name)}" id="tab-${name}">${title}</a></li>
		% endfor
	</ul>
</div>