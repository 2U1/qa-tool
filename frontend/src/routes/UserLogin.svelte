<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from '../components/Error.svelte'
    import { access_token, username, is_login } from '../lib/store'

    let error = {detail:[]}
    let login_username = ''
    let login_password = ''

    function login(event){
        event.preventDefault()
        let url = "/api/user/login"
        let params = {
            username: login_username,
            password: login_password,
        }

        fastapi('login', url, params,
            (json) => {
                $access_token = json.access_token
                $username = json.username
                $is_login = true
                push('/')
            },
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">Login</h5>
    <Error error={error} />
    <form method="post">
        <div class="mb-3">
            <label for="username">Username</label>
            <input type="text" class="form-control" bind:value="{login_username}" id="username" placeholder="Enter username">
        </div>
        <div class="mb-3">
            <label for="password">Password</label>
            <input type="password" class="form-control" bind:value="{login_password}" id="password" placeholder="Enter password">
        </div>
        <button type="submit" class="btn btn-dark" on:click="{login}">Login</button>
</div>