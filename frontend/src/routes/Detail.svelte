<script>
    import fastapi from "../lib/api"
    import { push } from 'svelte-spa-router'

    export let params ={}
    let data_idx = params.data_idx

    let _url = import.meta.env.VITE_SERVER_URL + '/api/dataset/vlm/image/'

    let data = {}

    let first_data_idx = 0
    let last_data_idx = 0

    let total = 0
    let checkedCount = 0
    $: checkedPercentage = total > 0 ? (checkedCount / total) * 100 : 0;
    $: conversations = data.conversations || [];

    function updateStatementQuality(idx, qualityValue, event) {
        event.preventDefault()
        let url = "/api/dataset/vlm/quality/" + data_idx
        let params = {
            "quality": qualityValue,
            "index": idx
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
    
    function getSpeakerIcon(speaker) {
        return speaker === 'gpt' ? 'robot.svg' : 'human.svg';
    }

    get_data()
    get_data_idx()
    $: get_dataset_progress()
</script>

<style>
    .conversation-item {
        display: flex;
        align-items: center; /* This will align children vertically */
        justify-content: space-between; /* This will push the buttons to the end */
    }

    .speaker-content {
        display: flex;
        align-items: center; /* This will align the icon with the text */
        gap: 10px;
        flex-grow: 1; /* This will allow the speaker content to grow and fill space */
    }

    .speaker-icon {
        width: 30px;
        height: 30px;
        flex-shrink: 0; /* Prevent the icon from shrinking */
    }

    .text-container p {
        margin: 0;
        line-height: 30px; /* Adjust this to ensure alignment with the icon */
    }

    .buttons-container {
        flex-shrink: 0; /* Prevent the buttons from shrinking */
        margin-left: auto; /* This pushes the button container to the right */
    }

</style>

<div class="container my-3">
    <div class="progress mb-3">
        <div class="progress-bar" role="progressbar" style="width: {checkedPercentage}%;" aria-valuenow="{checkedPercentage}" aria-valuemin="0" aria-valuemax="100">{Math.round(checkedPercentage)}%</div>
    </div>
    <!-- Info Section for Quality and Checked -->
    <div style="position: absolute; top: 50px; right: 0; padding: 10px;">
        <p style="color: {data.check ? 'green' : 'red'}">Checked: {data.check ? 'True' : 'False'}</p>
    </div>
    {#if data.image}
    <div align="center">
        <img src={_url+data.image} alt={_url+data.image} height="350">
    </div>
    {/if}
    <div class="card my-3" align="center">
        <div class="card-body">
            {#each conversations as conversation, idx (conversation.index)}
                <div class="mb-3 conversation-item">
                    <div class="speaker-content">
                        <img class="speaker-icon" src={`/${getSpeakerIcon(conversation.speaker)}`} alt={conversation.speaker}/>
                        <div class="text-container">
                            <p><strong>{conversation.speaker}: </strong>{conversation.value}</p>
                        </div>
                    </div>
                    <div class="buttons-container">
                        <button on:click={(event) => updateStatementQuality(idx, true, event)}
                            class="btn {conversation.quality === false ? 'btn-secondary' : 'btn-success'}">
                        Accept
                        </button>
                        <button on:click={(event) => updateStatementQuality(idx, false, event)}
                                class="btn {conversation.quality === true ? 'btn-secondary' : 'btn-danger'}">
                            Reject
                        </button>
                    </div>
                </div>
            {/each}
        </div>
    </div>
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