<%inherit file="/base.mao" />
<h2>Home</h2>
<div id="latest-projects">
	<h3>Latest projects</h3>
	<ul>
		% for project in c.latest_projects:
		<li>
			<a href="${h.url_for(controller='projects', action='show', project=project.identifier)}">${project.name}</a> (${project.created_on})
			<p>${project.description}</p>
		</li>
		% endfor
	</ul>
</div>
<p>
	Testing testing 1 2 3
</p>
