<%inherit file="/base.mao" />
<h2>Login</h2>
<form id="login">
    <label for="username">Username:</label>
    ${h.tags.text('username')}
    
    <label for="password">Password:</label>
    ${h.tags.text('password')}
    
    <a href="${h.url_for(action='lost_password')}" class="lost_password">Lost password</a>
    <button>Login &raquo;</button>
    <br style="clear: both;" />
</form>