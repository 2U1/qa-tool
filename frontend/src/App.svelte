<script>
    import Router from 'svelte-spa-router'
    import Home from './routes/Home.svelte'
    import Detail from './routes/Detail.svelte'
    import Navigation from './components/Navigation.svelte'
    import UserCreate from './routes/UserCreate.svelte'
    import UserLogin from './routes/UserLogin.svelte'
    import Upload from './routes/Upload.svelte'

    const routes = {
        '/': Home,
        '/detail/:data_idx':Detail,
        '/user-create': UserCreate,
        '/user-login': UserLogin,
        '/upload': Upload,
    }
</script>

<Navigation />
<Router {routes}/>