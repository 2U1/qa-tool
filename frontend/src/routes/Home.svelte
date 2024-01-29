<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import moment from 'moment/min/moment-with-locales'
    import { page } from '../lib/store'
    
    moment.locale('ko')
    
    let dataset_list = []
    let size = 10
    let total = 0
    $: total_page = Math.ceil(total / size)

    function get_dataset_list(_page) {
        let params = {
            page: _page,
            size: size,
        }
        
        fastapi('get','/api/dataset/vlm/list', params, (json) => {
            dataset_list = json.dataset_list
            $page = _page
            total = json.total
        })   
    }

    $: get_dataset_list($page)
</script>

<div class="container my-3">
    <table class="table">
        <thead>
            <tr class="table-dark">
                <th scope="col">Index</th>
                <th scope="col">Image</th>
                <th scope="col">Check</th>
                <th scope="col">Date</th>
                <th scope="col">Detail</th>
            </tr>
        </thead>
        <tbody>
            {#each dataset_list as dataset}
                <tr>
                    <th scope="row">{dataset.idx}</th>
                    <td><img src="/images/{dataset.image}" alt="/images/{dataset.image}" width="100px"></td>
                    <td>{dataset.check}</td>
                    <td>{moment(dataset.date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
                    <td><a use:link href="/detail/{dataset.idx}">[이동]</a></td>
                </tr>
            {/each}
        </tbody>
    </table>

    <ul class="pagination justify-content-center">
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => get_dataset_list($page-1)}">Previous</button>
        </li>
        {#each Array(total_page) as _, loop_page}
        {#if loop_page > $page-3 && loop_page < $page+3}
        <li class="page-item {loop_page === $page && 'active'}">
            <button class="page-link" on:click="{() => get_dataset_list(loop_page)}">{loop_page+1}</button>
        </li>
        {/if}
        {/each}
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => get_dataset_list($page+1)}">Next</button>
    </ul>
</div>