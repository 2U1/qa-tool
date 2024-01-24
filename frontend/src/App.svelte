<script>
    let dataset_list = []

    function get_dataset_list() {
        fetch('http://localhost:30120/api/dataset/vlm/list')
            .then((response) => {response.json()
                .then((json) => {
                    dataset_list = json
                })
            })
        }

    get_dataset_list()
</script>

<ul>
    {#each dataset_list as dataset}
        <li>{dataset.image}</li>
    {/each}
</ul>