<script lang="ts">  
  import { resolve } from '$app/paths';  
  import { goto } from '$app/navigation';  


  function navigate_to_gallery() {  
    goto(resolve('/gallery'));  
  }  
</script>  

<nav>  
   

  <div class="navigators">  
    <button on:click={navigate_to_gallery}>Gallery</button>  
  </div>  
</nav>  

<style>  
  nav {  
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    display: flex;  
    flex-direction: row; 
    justify-content: end;  
    align-items: center;
    padding: 0 1rem;  
    height: 10vh;
    box-sizing: border-box;
    z-index: 1000;
    overflow: hidden;
  }

  

  .navigators {
    display: flex;
    align-items: center;
    height: 100%;
  }

  button {  
    cursor: pointer;  
    padding: 0.5rem 1rem;
    font-size: 1rem;
    white-space: nowrap;
  }  

  @media (max-width: 600px) {
    
    button {
      padding: 0.4rem 0.8rem;
      font-size: 0.9rem;
    }
  }
</style>