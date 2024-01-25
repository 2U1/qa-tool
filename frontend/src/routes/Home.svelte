<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    
    let dataset_list = []

    function get_dataset_list() {
        fastapi('get','/api/dataset/vlm/list', {}, (json) => {
            dataset_list = json
        })   
    }

    get_dataset_list()
</script>

<ul>
    {#each dataset_list as dataset}
        <li><a use:link href="/detail/{dataset.idx}">{dataset.idx}</a></li>
    {/each}
</ul>