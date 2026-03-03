<script lang="ts">
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';

  interface Picture {
    download_url: string;
    id: string;
    author: string;
    width: number;
    height: number;
    url: string;
  }

  let pictures: Picture[] = [];
  let loading = true;
  let downloadingId: string | null = null;
  let notification: string | null = null;

  const selectedImage = writable<Picture | null>(null);
  const selectedIndex = writable<number>(-1);

  onMount(async () => {
    try {
      const res = await fetch("https://picsum.photos/v2/list?limit=80&page=1");
      pictures = await res.json();
    } catch (e) {
      console.error("Failed to fetch images", e);
    } finally {
      loading = false;
    }
  });

  function openImage(picture: Picture, index: number) {
    selectedImage.set(picture);
    selectedIndex.set(index);
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    selectedImage.set(null);
    selectedIndex.set(-1);
    document.body.style.overflow = '';
  }

  function navigate(direction: 1 | -1) {
    selectedIndex.update(i => {
      const next = i + direction;
      if (next < 0 || next >= pictures.length) return i;
      selectedImage.set(pictures[next]);
      return next;
    });
  }

  function handleKeydown(e: KeyboardEvent) {
    if (!$selectedImage) return;
    if (e.key === 'Escape') closeModal();
    if (e.key === 'ArrowRight') navigate(1);
    if (e.key === 'ArrowLeft') navigate(-1);
  }

  function handleModalClick(e: MouseEvent) {
    if ((e.target as HTMLElement).classList.contains('modal-backdrop')) closeModal();
  }

  async function downloadImage(picture: Picture, e: MouseEvent) {
    e.stopPropagation();
    downloadingId = picture.id;

    try {
      // Force a real download via blob
      const response = await fetch(picture.download_url);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `photo-${picture.id}-by-${picture.author.replace(/\s+/g, '-')}.jpg`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showNotification('Download started!');
    } catch (err) {
      showNotification('Download failed — try again.');
    } finally {
      downloadingId = null;
    }
  }

  function showNotification(msg: string) {
    notification = msg;
    setTimeout(() => { notification = null; }, 2800);
  }

  // Intersection Observer–based lazy load
  function lazyLoad(node: HTMLImageElement, src: string) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            node.src = src;
            node.classList.add('loaded');
            observer.disconnect();
          }
        });
      },
      { rootMargin: '200px' }
    );
    observer.observe(node);
    return {
      destroy() { observer.disconnect(); }
    };
  }

  // Thumbnail URL helper (small size for grid)
  function thumbUrl(picture: Picture): string {
    return `https://picsum.photos/id/${picture.id}/400/300`;
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<main>
  <!-- Header -->
  <header>
    <div class="header-inner">
      <p class="brand-tagline">Curated photography from Mangu Christian Union</p>
    </div>
  </header>

  <!-- Skeleton or gallery -->
  {#if loading}
    <div class="grid">
      {#each Array(24) as _}
        <div class="card skeleton">
          <div class="skeleton-img"></div>
          <div class="skeleton-footer">
            <div class="skeleton-line short"></div>
            <div class="skeleton-line"></div>
          </div>
        </div>
      {/each}
    </div>
  {:else}
    <div class="grid">
      {#each pictures as picture, i}
        <div class="card" on:click={() => openImage(picture, i)} on:keydown={(e) => e.key === 'Enter' && openImage(picture, i)} role="button" tabindex="0">
          <div class="card-img-wrap">
            <!-- Placeholder blur -->
            <img
              class="thumb-placeholder"
              src={`https://picsum.photos/id/${picture.id}/20/15`}
              alt=""
              aria-hidden="true"
            />
            <!-- Actual lazy-loaded image -->
            <img
              class="thumb"
              src=""
              use:lazyLoad={thumbUrl(picture)}
              alt="Photo by {picture.author}"
            />
            <div class="card-overlay">
              <button
                class="btn-download"
                on:click={(e) => downloadImage(picture, e)}
                aria-label="Download photo by {picture.author}"
                disabled={downloadingId === picture.id}
              >
                {#if downloadingId === picture.id}
                  <span class="spinner"></span>
                {:else}
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                {/if}
              </button>
              <div class="expand-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Modal lightbox -->
  {#if $selectedImage}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="modal-backdrop" on:click={handleModalClick} role="dialog" aria-modal="true" tabindex="-1">
      <div class="modal-content">
        <img src={$selectedImage.download_url} alt="Photo by {$selectedImage.author}" />

        <!-- Info bar -->
        <div class="modal-info">
          
          <button class="btn-modal-download" on:click={(e) => downloadImage($selectedImage, e)}>
            {#if downloadingId === $selectedImage.id}
              <span class="spinner"></span> Downloading…
            {:else}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Download
            {/if}
          </button>
        </div>

        <!-- Nav buttons -->
        {#if $selectedIndex > 0}
          <button class="nav-btn prev" on:click|stopPropagation={() => navigate(-1)} aria-label="Previous">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
        {/if}
        {#if $selectedIndex < pictures.length - 1}
          <button class="nav-btn next" on:click|stopPropagation={() => navigate(1)} aria-label="Next">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
        {/if}

        <!-- Close -->
        <button class="modal-close" on:click={closeModal} aria-label="Close">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
    </div>
  {/if}

  <!-- Toast notification -->
  {#if notification}
    <div class="toast" role="status">{notification}</div>
  {/if}
</main>

<style>
  :global(*, *::before, *::after) { box-sizing: border-box; margin: 0; padding: 0; }
  :global(body) { background-color: #f5e104; color: #e8e8e8; font-family: 'Inter', system-ui, -apple-system, sans-serif; }

  /* ── HEADER ─────────────────────────────── */
  header {
    background: linear-gradient(180deg, #e0f403 0%, transparent 100%);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 2rem 2.5rem 1.6rem;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }
  .header-inner { max-width: 1600px; margin: 0 auto; }
  .brand-tagline { font-size: 0.8rem; color: #0a0a0a; letter-spacing: 0.04em; text-transform: uppercase; }

  /* ── GRID ────────────────────────────────── */
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1px;
    background: #1a1a1e;
    padding: 1px;
    max-width: 1600px;
    margin: 0 auto;
  }

  /* ── CARD ────────────────────────────────── */
  .card {
    background: #111113;
    cursor: pointer;
    outline: none;
    position: relative;
    transition: z-index 0s;
    margin-bottom: 3vh;
    margin-right: 1vw;
  }
  .card:focus-visible { box-shadow: inset 0 0 0 2px #a78bfa; }

  .card-img-wrap {
    position: relative;
    overflow: hidden;
    aspect-ratio: 4/3;
    background: #1c1c20;
  }

  /* Blurry placeholder */
  .thumb-placeholder {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: blur(12px);
    transform: scale(1.05);
    transition: opacity 0.4s ease;
  }
  .thumb {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 1;
    transition: opacity 0.5s ease, transform 0.5s ease;
  }
  

  /* Hover overlay */
  .card-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0) 50%, rgba(0,0,0,0.72) 100%);
    opacity: 0;
    transition: opacity 0.25s ease;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    padding: 0.75rem;
  }
  .card:hover .card-overlay { opacity: 1; }

  .expand-icon {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0.85);
    transition: transform 0.2s ease;
    color: rgba(255,255,255,0.8);
    pointer-events: none;
  }
  .expand-icon svg { width: 28px; height: 28px; }
  .card:hover .expand-icon { transform: translate(-50%, -50%) scale(1); }

  /* Download button on card */
  .btn-download {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.18);
    color: #fff;
    border-radius: 8px;
    padding: 0.45rem 0.55rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s, border-color 0.2s, transform 0.15s;
    position: relative;
    z-index: 2;
  }
  .btn-download svg { width: 16px; height: 16px; }
  .btn-download:hover { background: rgba(167,139,250,0.35); border-color: #a78bfa; transform: scale(1.07); }
  .btn-download:disabled { opacity: 0.6; cursor: wait; }

  /* Card footer */
    .skeleton-img {
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, #1c1c20 25%, #252529 50%, #1c1c20 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 0;
  }
  .skeleton-footer { padding: 0.65rem 0.85rem; display: flex; flex-direction: column; gap: 0.4rem; }
  .skeleton-line {
    height: 10px;
    border-radius: 4px;
    background: linear-gradient(90deg, #1c1c20 25%, #252529 50%, #1c1c20 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
  }
  .skeleton-line.short { width: 55%; }
  @keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }

  /* ── MODAL ───────────────────────────────── */
  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(5, 5, 8, 0.94);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: fadeIn 0.2s ease;
  }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

  .modal-content {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: min(92vw, 1100px);
    max-height: 92vh;
    animation: scaleIn 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  @keyframes scaleIn { from { transform: scale(0.93); opacity: 0; } to { transform: scale(1); opacity: 1; } }

  .modal-content img {
    max-width: 100%;
    max-height: calc(92vh - 60px);
    object-fit: contain;
    border-radius: 4px;
    display: block;
    box-shadow: 0 32px 80px rgba(0,0,0,0.8);
  }

  .modal-info {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 0.2rem 0;
  }
  .modal-author {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #9a9aaa;
  }
  .modal-author svg { width: 14px; height: 14px; }

  .btn-modal-download {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #a78bfa;
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.1rem;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, transform 0.15s;
    letter-spacing: 0.01em;
  }
  .btn-modal-download svg { width: 15px; height: 15px; }
  .btn-modal-download:hover { background: #9166f0; transform: translateY(-1px); }
  .btn-modal-download:disabled { opacity: 0.6; cursor: wait; }

  /* Nav arrows */
  .nav-btn {
    position: absolute;
    top: calc(50% - 30px);
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #fff;
    border-radius: 50%;
    width: 46px;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.2s, transform 0.15s;
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
  }
  .nav-btn svg { width: 20px; height: 20px; }
  .nav-btn:hover { background: rgba(167,139,250,0.3); border-color: #a78bfa; transform: scale(1.08); }
  .prev { left: -64px; }
  .next { right: -64px; }

  /* Close button */
  .modal-close {
    position: absolute;
    top: -48px;
    right: 0;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #fff;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.2s, transform 0.15s;
  }
  .modal-close svg { width: 16px; height: 16px; }
  .modal-close:hover { background: rgba(239,68,68,0.3); border-color: #ef4444; transform: rotate(90deg); }

  /* ── TOAST ───────────────────────────────── */
  .toast {
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    background: #1f1f24;
    border: 1px solid rgba(167,139,250,0.35);
    color: #e8e8e8;
    padding: 0.7rem 1.4rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 500;
    z-index: 2000;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    animation: toastIn 0.25s ease, toastOut 0.3s ease 2.5s forwards;
    white-space: nowrap;
  }
  @keyframes toastIn { from { opacity: 0; transform: translateX(-50%) translateY(12px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
  @keyframes toastOut { from { opacity: 1; } to { opacity: 0; } }

  /* ── SPINNER ─────────────────────────────── */
  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
    display: inline-block;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* ── RESPONSIVE ──────────────────────────── */
  @media (max-width: 900px) {
    .prev { left: -48px; }
    .next { right: -48px; }
  }
  @media (max-width: 640px) {
    .grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }
    .prev, .next { display: none; }
    header { padding: 1.2rem 1rem 1rem; }
    .modal-content { max-width: 100vw; max-height: 100vh; border-radius: 0; }
    .modal-content img { max-height: calc(100vh - 80px); }
    .modal-close { top: 0.5rem; right: 0.5rem; position: fixed; }
  }
</style>