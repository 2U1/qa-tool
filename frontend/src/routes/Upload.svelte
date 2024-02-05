<script>
    import fastapi from "../lib/api";
  
    let file;
    let options = ["VLM"];
  
    function upload_dataset() {
      if (!file) {
        console.error("No file selected");
        return;
      }
  
      let formData = new FormData();
      formData.append('file', file);
  
      fastapi('post', '/api/dataset/vlm/upload', formData, (json) => {
          console.log(json);
      });
    }
  
    function selectFile() {
      document.getElementById('fileInput').click();
    }
  
    function handleFileChange(event) {
      file = event.target.files[0];
      if (file) {
        upload_dataset();
      }
    }
  </script>

<style>
    .upload-cell {
      text-align: right;
    }
  </style>
  
  <div class="container my-3">
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
                          <button type="button" class="btn btn-dark mb-2" on:click={selectFile}>Upload</button>
                          <input type="file" id="fileInput" on:change={handleFileChange} style="display: none;" />
                      </td>
                  </tr>
              {/each}
          </tbody>
      </table>
  </div>