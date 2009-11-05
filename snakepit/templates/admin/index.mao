<%inherit file="/base.mao" />
<h2>Administration</h2>
<ul>
    <li><a href="${h.url_for(action='projects')}">Projects</a> | <a href="${h.url_for(controller='projects', action='add')}">New</a></li>
</ul>