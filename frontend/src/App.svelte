<script>
    import Router from 'svelte-spa-router'
    import Home from './routes/Home.svelte'
    import Detail from './routes/Detail.svelte'
    import Navigation from './components/Navigation.svelte';

    const routes = {
        '/': Home,
        '/detail/:data_idx':Detail,
    }
</script>

<Navigation />
<Router {routes}/>