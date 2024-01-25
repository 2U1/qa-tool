<script>
    import fastapi from "../lib/api"

    export let params ={}
    let data_idx = params.data_idx

    let data = {}

    function get_data() {
        fastapi("get", "/api/dataset/vlm/" + data_idx, {}, (json) =>{
            data = json
        })
    }

    function update_quality(qualityValue) {
        let url = "/api/dataset/vlm/quality/" + data_idx
        let params = {
            "quality": qualityValue
        }
        fastapi('put', url, params,
            (json) => {
                // data_idx += 1
                // get_data()
                console.log(json)
            }
        )
    }

    get_data()
</script>

<h1>{data.idx}</h1>
<div>
    {data.image}
</div>
<div>
    {data.human}
</div>
<div>
    {data.gpt}
</div>

<div>
    <button on:click={() => update_quality(true)}>Accept</button>
    <button on:click={() => update_quality(false)}>Reject</button>
</div>
