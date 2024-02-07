<script>
  import fastapi from "../lib/api";

  let file;
  let options = ["VLM"];
  let isLoading = false;

  let selectedDatasetName;

  async function upload_dataset(datasetName) {
    if (!file) {
      console.error("No file selected");
      return;
    }

    isLoading = true;

    datasetName = datasetName.toLowerCase();
    
    let formData = new FormData();
    formData.append('file', file);

    try {
      const json = await fastapi('post', '/api/dataset/'+datasetName+'/upload', formData);
      console.log(json);
    } catch (error) {
      console.error("Error during upload:", error);
    } finally {
      isLoading = false;
    }
  }

  function selectFile(datasetName) {
    selectedDatasetName = datasetName;
    document.getElementById('fileInput').click();
  }

  function handleFileChange(event) {
    file = event.target.files[0];
    if (file) {
      upload_dataset(selectedDatasetName);
    }
  }
</script>

<style>
  .loading-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
  }

  .loader {
    border: 16px solid #f3f3f3;
    border-top: 16px solid #3498db;
    border-radius: 50%;
    width: 120px;
    height: 120px;
    animation: spin 2s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
  
<div class="container my-3">
  {#if isLoading}
    <div class="loading-screen">
      <div class="loader"></div>
    </div>
  {:else}
    <table class="table">
      <thead>
          <tr class="table-dark">
              <th scope="col">Dataset</th>
              <th scope="col"></th> 
          </tr>
      </thead>
      <tbody>
          {#each options as opt}
              <tr>
                  <th scope="row">{opt}</th>
                  <td class="upload-cell">
                      <button type="button" class="btn btn-dark mb-2" on:click={() => selectFile(opt)}>Upload</button>
                      <input type="file" id="fileInput" on:change={handleFileChange} style="display: none;" />
                  </td>
              </tr>
          {/each}
      </tbody>
    </table>
  {/if}

</div>