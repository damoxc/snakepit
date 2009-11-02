<%inherit file="/base.mao" />
<h2>Login</h2>
<form id="login">
    <label for="username">Username</label>
    ${h.tags.text('username')}
    
    <label for="password">Password</label>
    ${h.tags.text('password')}
    
    <button>Login</button>
</form>