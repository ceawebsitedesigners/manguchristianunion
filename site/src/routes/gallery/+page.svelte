<script lang="ts">
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';

  let pictures: { download_url: string; id: string; author: string }[] = [];
  const selectedImage = writable<{ download_url: string; id: string; author: string } | null>(null);

  // Fetch images on mount
  onMount(async () => {
    const res = await fetch("https://picsum.photos/v2/list");
    pictures = await res.json();
  });

  // Open modal
  function openImage(picture) {
    selectedImage.set(picture);
  }

  // Close modal
  function closeModal() {
    selectedImage.set(null);
  }
</script>

<section>
  <div id="pictures">
    {#each pictures as picture}
      <div class="image-card">
        <img 
          src={picture.download_url} 
          alt="Picture {picture.id}" 
          loading="lazy" 
          on:click={() => openImage(picture)} 
        />
        <a class="download-btn" href={picture.download_url} download={`image_${picture.id}.jpg`}>
          Download
        </a>
      </div>
    {/each}
  </div>

  {#if $selectedImage}
    <div class="modal" on:click={closeModal}>
      <img src={$selectedImage.download_url} alt="Fullscreen image" />
    </div>
  {/if}
</section>

<style>
  section {
    padding: 1rem;
  }

  #pictures {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }

  .image-card {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
  }

  .image-card img {
    width: 100%;
    height: auto;
    object-fit: cover;
    cursor: pointer;
    transition: transform 0.3s ease;
  }

  .image-card img:hover {
    transform: scale(1.05);
  }

  .download-btn {
    position: absolute;
    bottom: 8px;
    right: 8px;
    background: rgba(0,0,0,0.6);
    color: white;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    text-decoration: none;
  }

  /* Fullscreen modal */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.85);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    cursor: pointer;
  }

  .modal img {
    max-width: 95%;
    max-height: 95%;
    object-fit: contain;
  }

  /* Make grid adapt to screen width */
  @media (max-width: 600px) {
    #pictures {
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    }
  }
</style>