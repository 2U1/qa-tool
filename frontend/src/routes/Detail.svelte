<script>
    import fastapi from "../lib/api"
    import { push } from 'svelte-spa-router'

    export let params ={}
    let data_idx = params.data_idx

    let image_src = "/images/"

    let data = {}

    let first_data_idx = 0
    let last_data_idx = 0

    let total = 0
    let checkedCount = 0
    $: checkedPercentage = total > 0 ? (checkedCount / total) * 100 : 0;


    function get_data() {
        fastapi("get", "/api/dataset/vlm/detail/" + data_idx, {}, (json) =>{
            data = json
        })
    }

    function get_dataset_progress() {
        fastapi('get','/api/dataset/vlm/list/progress', {}, (json) => {
            total = json.total
            checkedCount = json.progress
        })   
    }

    function get_data_idx() {
        fastapi("get", "/api/dataset/vlm/info/idx", {}, (json) =>{
            first_data_idx = json.first_idx
            last_data_idx = json.last_idx
        })
    }

    function move_to_prev_next_data_idx(direction) {
        if (direction == "prev") {
            if (data_idx == first_data_idx) {
                alert("This is the first data")
            } else {
                data_idx -= 1
                get_data()
            }
        } else if (direction == "next") {
            if (data_idx == last_data_idx) {
                alert("This is the last data")
            } else {
                data_idx += 1
                get_data()
            }
        }
    }

    function update_quality(qualityValue, event) {
        event.preventDefault()
        let url = "/api/dataset/vlm/quality/" + data_idx
        let params = {
            "quality": qualityValue
        }
        
        try {
        fastapi('put', url, params, (json) => {
            get_data()
            get_dataset_progress()
        })
        } catch (error) {
            console.error("Error during update:", error)
            alert("An error occurred: " + error.message)
        }

    }

    get_data()
    get_data_idx()
    $: get_dataset_progress()
</script>

<div class="container my-3">
    <div class="progress mb-3">
        <div class="progress-bar" role="progressbar" style="width: {checkedPercentage}%;" aria-valuenow="{checkedPercentage}" aria-valuemin="0" aria-valuemax="100">{Math.round(checkedPercentage)}%</div>
    </div>
    <!-- Info Section for Quality and Checked -->
    <div style="position: absolute; top: 50px; right: 0; padding: 10px;">
        <p style="color: {data.check ? 'green' : 'red'}">Checked: {data.check ? 'True' : 'False'}</p>
    </div>
    <div align="center">
        <img src={image_src+data.image} alt={image_src+data.image} height="350">
    </div>
    <div class="card my-3" align="center">
        <div class="card-body">
            <h2 class="card-title">Human</h2>
            <div class="card-text" style="white-space: pre-line;">{data.human}</div>
        </div>
    </div>
    <div class="card my-3" align="center">
        <div class="card-body">
            <h2 class="card-title">GPT</h2>
            <div class="card-text" style="white-space: pre-line;">{data.gpt}</div>
        </div>
    </div>
</div>

<div align="center">
    <button type="button"
            class="btn {data.quality === false ? 'btn-secondary' : 'btn-success'}"
            on:click={(event) => update_quality(true, event)}
            style="opacity:0.9;">
        Accept
    </button>
    <button type="button"
            class="btn {data.quality === true ? 'btn-secondary' : 'btn-danger'}"
            on:click={(event) => update_quality(false, event)}
            style="opacity:0.9;">
        Reject
    </button>
</div>

<div class="container my-5">
    <div class="row">
        <div class="col text-start">
            <button type="button" class="btn btn-dark mb-2" on:click="{() => {push('/')}}">List</button>
        </div>
        <div class="col text-end">
            <button type="button" class="btn btn-primary" on:click="{() => move_to_prev_next_data_idx("prev")}">Previous</button>
            <button type="button" class="btn btn-primary" on:click="{() => move_to_prev_next_data_idx("next")}">Next</button>
        </div> 
    </div>
</div>