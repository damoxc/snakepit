<%inherit file="/base.mao" />
<h2>New project</h2>
% if c.error:
	<div class="error">${c.error}</div>
% endif
<form action="${h.url_for()}" method="POST">
	<label for="name">Name ${h.required()}</label>
	${h.tags.text('name', c.name)}
	<span class="description">30 characters maximum.</span>

	<label for="description">Description</label>
	${h.tags.textarea('description', c.description)}

	<label for="identifier">Identifier ${h.required()}</label>
	${h.tags.text('identifier', c.identifier)}
	<span class="description">
		Length between 1 and 20 characters. Only lower case letters (a-z), numbers and dashes are allowed.<br/>
		Once saved, the identifier can not be changed.
	</span>

	<label for="homepage">Homepage</label>
	${h.tags.text('homepage', c.homepage)}

	<label for="is_public">Public</label>
	${h.tags.checkbox('is_public', checked=c.is_public or True)}

	<button>Create &raquo;</button>
</form>