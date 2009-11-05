<%inherit file="/base.mao" />
<h2>Projects</h2>
% for project in c.projects:
    <h3>
        <a class="icon icon-fav" href="${h.url_for(action='show', id=project.identifier)}">${project.name}</a>
    </h3>
    <p>${project.description}</p>
% endfor