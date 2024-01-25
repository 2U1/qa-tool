<script>
    import Router from 'svelte-spa-router'
    import Home from './routes/Home.svelte'
    import Detail from './routes/Detail.svelte'

    const routes = {
        '/': Home,
        '/detail/:data_idx':Detail,
    }
</script>


<Router {routes}/>