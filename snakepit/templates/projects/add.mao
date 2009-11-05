<%inherit file="/base.mao" />
<h2>New project</h2>
<form action="${h.url_for()}" method="POST">
	<label>Name ${h.required()}</label>
	${h.tags.text('name')}
	<span class="description">30 characters maximum.</span>

	<label>Description</label>
	${h.tags.textarea('description')}

	<label>Identifier ${h.required()}</label>
	${h.tags.text('identifier')}
	<span class="description">
		Length between 1 and 20 characters. Only lower case letters (a-z), numbers and dashes are allowed.<br/>
		Once saved, the identifier can not be changed.
	</span>

	<label>Homepage</label>
	${h.tags.text('homepage')}

	<label>Public</label>
	${h.tags.checkbox('public', checked=c.public or True)}

	<button>Create &raquo;</button>
</form>