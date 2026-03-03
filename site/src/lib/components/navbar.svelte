<script lang="ts">  
  import { base } from '$app/paths';  
  import { goto } from '$app/navigation';  
  import img from '$lib/assets/hero-church.jpg';  

  function navigate_to_gallery() {  
    goto(`${base}/gallery`);  
  }  
</script>  

<nav>  
  <div class="decoration">  
    <!-- <img src={img} alt="logo" class="logo">   -->
  </div>  

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
    justify-content: space-between;  
    align-items: center;
    padding: 0 1rem;  
    height: 10vh;
    box-sizing: border-box;
    z-index: 1000;
    overflow: hidden;
  }

  .decoration {
    display: flex;
    align-items: center;
    height: 100%;
  }

  .logo { 
    height: 60%;
    width: auto; 
    display: block;
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
    .logo {
      height: 50%;
    }
    button {
      padding: 0.4rem 0.8rem;
      font-size: 0.9rem;
    }
  }
</style>