<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import moment from 'moment/min/moment-with-locales'
    import { page, check_filter } from '../lib/store'
    
    moment.locale('ko')
    
    let dataset_list = []
    let size = 10
    let total = 0
    let checkedCount = 0
    $: total_page = Math.ceil(total / size)
    $: checkedPercentage = total > 0 ? (checkedCount / total) * 100 : 0;

    let _url = import.meta.env.VITE_SERVER_URL + '/api/dataset/vlm/image/'
    
    function get_dataset_list(_page, _check_filter) {
        let params = {
            page: _page,
            size: size,
            check: _check_filter
        }
        
        fastapi('get','/api/dataset/vlm/list', params, (json) => {
            dataset_list = json.dataset_list
            $page = _page
            total = json.total
        })   
    }

    function get_dataset_progress() {
        fastapi('get','/api/dataset/vlm/list/progress', {}, (json) => {
            checkedCount = json.progress
        })   
    }

    $: get_dataset_list($page, $check_filter)
    $: get_dataset_progress()
</script>

<div class="container my-3">
    <div class="mb-3">
        <div class="progress mb-3">
            <div class="progress-bar" role="progressbar" style="width: {checkedPercentage}%;" aria-valuenow="{checkedPercentage}" aria-valuemin="0" aria-valuemax="100">{Math.round(checkedPercentage)}%</div>
        </div>
        <select class="form-select" bind:value={$check_filter}>
            <option value="all">All</option>
            <option value="true">Checked</option>
            <option value="false">Unchecked</option>
        </select>
    </div>
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
                    <td><img src={_url + dataset.image} alt={dataset.image} width="100px"></td>
                    <td style="color: {dataset.check ? 'green' : 'red'}">{dataset.check ? 'True' : 'False'}</td>
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