<%inherit file="/project.mao" />
% if not c.page:
<h2>${c.title}</h2>
<p>
    This page doesn't exist. <a href="${h.url_for(edit='edit')}">Create</a> it?
</p>
% else:
<h2>${c.page.title}</h2>
% endif