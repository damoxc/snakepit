<%inherit file="/project.mao" />
<h2>Overview</h2>
<div class="description">
	${c.project.description}
</div>
<ul>
	<li>Homepage: ${h.tags.link_to(c.project.homepage, c.project.homepage)}</li>
</ul>