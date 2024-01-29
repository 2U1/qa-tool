<script>
    import fastapi from "../lib/api"
    import { push } from 'svelte-spa-router'

    export let params ={}
    let data_idx = params.data_idx

    let image_src = "/images/"

    let data = {}

    let first_data_idx = 0
    let last_data_idx = 0

    function get_data() {
        fastapi("get", "/api/dataset/vlm/detail/" + data_idx, {}, (json) =>{
            data = json
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

    function update_quality(qualityValue) {
        let url = "/api/dataset/vlm/quality/" + data_idx
        let params = {
            "quality": qualityValue
        }
        
        try {
        fastapi('put', url, params)
        // alert("Update Success")
        } catch (error) {
            console.error("Error during update:", error)
            alert("An error occurred: " + error.message)
        }

    }

    get_data()
    get_data_idx()
</script>

<!-- <div class="container mt-3">
    <div class="row">
        <div class="col text-end">
            <button type="button" class="btn btn-dark mb-2" on:click="{() => {push('/')}}">List</button>
        </div>
    </div>
</div> -->

<div class="container my-3">
    <div align="center">
    <img src={image_src+data.image} alt={image_src+data.image} height="350">
    </div>
    <!-- <div class="card my-3" align="center">
        <div class="card-body">
            <h2 class="card-title">Human</h2>
            <div class="card-text" style="white-space: pre-line;">{data.human}</div>
        </div>
    </div> -->
    <div class="card my-3" align="center">
        <div class="card-body">
            <h2 class="card-title">GPT</h2>
            <div class="card-text" style="white-space: pre-line;">{data.gpt}</div>
        </div>
    </div>
</div>

<div align="center">
    <button type="button" class="btn btn-success" on:click={() => update_quality(true)}>Accept</button>
    <button type="button" class="btn btn-danger" on:click={() => update_quality(false)}>Reject</button>
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