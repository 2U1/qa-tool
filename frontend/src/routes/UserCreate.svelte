<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from '../components/Error.svelte'
    
    let error = {detail:[]}
    let username = ''
    let password1 = ''
    let password2 = ''

    function post_user(event) {
        event.preventDefault()
        let url = "/api/user/create"
        let params = {
            username: username,
            password1: password1,
            password2: password2,
            idx: 0,
        }

        fastapi('post', url, params, 
        (json) => {
            push('/user-login')
        },
        (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">Sign up</h5>
    <Error error={error} />
    <form method="post">
        <div class="mb-3">
            <label for="username">Username</label>
            <input type="text" class="form-control" bind:value="{username}" id="username" placeholder="Enter username">
        </div>
        <div class="mb-3">
            <label for="password1">Password</label>
            <input type="password" class="form-control" bind:value="{password1}" id="password1" placeholder="Enter password">
        </div>
        <div class="mb-3">
            <label for="password2">Password Confirm</label>
            <input type="password" class="form-control" bind:value="{password2}" id="password2" placeholder="Enter password confirm">
        </div>
        <button type="submit" class="btn btn-dark" on:click="{post_user}">Sign up</button>
    </form>
</div>