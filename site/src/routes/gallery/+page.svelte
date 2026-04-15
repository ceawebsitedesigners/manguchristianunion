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
		public_id?: string;
	}

	// ── Config ──────────────────────────────────────────────────────────────
	import { URLS } from '$lib/urls';
	const AUTHOR = 'Mangu Christian Union';
	const FOLDER = 'Clients/manguchristianunion';

	let pictures: Picture[] = [];
	let loading = true;
	let loadingMore = false;
	let nextCursor: string | null = null;
	let downloadingId: string | null = null;
	let notification: string | null = null;
	let errorMsg: string | null = null;

	const selectedImage = writable<Picture | null>(null);
	const selectedIndex = writable<number>(-1);

	// ── Fetch images from Flask ──────────────────────────────────────────────
	async function fetchImages(cursor?: string) {
		try {
			const url = cursor ? URLS.mediaImagesNext(cursor, FOLDER) : URLS.mediaImages(FOLDER);

			const res = await fetch(url);
			if (!res.ok) throw new Error(`Server error: ${res.status}`);
			const data = await res.json();

			if (data.error) throw new Error(data.error);

			pictures = cursor ? [...pictures, ...data.pictures] : data.pictures;
			nextCursor = data.next_cursor ?? null;
		} catch (e: Error | unknown) {
			console.error('Failed to fetch images', e);
			errorMsg =
				(e instanceof Error ? e.message : String(e)) ??
				'Failed to load images. Check server connection.';
		}
	}

	onMount(async () => {
		await fetchImages();
		loading = false;
	});

	async function loadMore() {
		if (!nextCursor || loadingMore) return;
		loadingMore = true;
		await fetchImages(nextCursor);
		loadingMore = false;
	}

	// ── Modal helpers ─────────────────────────────────────────────────────────
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
		selectedIndex.update((i) => {
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

	// ── Download ──────────────────────────────────────────────────────────────
	async function downloadImage(picture: Picture, e: MouseEvent) {
		e.stopPropagation();
		downloadingId = picture.id;
		try {
			const response = await fetch(picture.download_url);
			const blob = await response.blob();
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = `mangu-cu-photo-${picture.id}.jpg`;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			URL.revokeObjectURL(url);
			showNotification('Download started!');
		} catch {
			showNotification('Download failed — try again.');
		} finally {
			downloadingId = null;
		}
	}

	function showNotification(msg: string) {
		notification = msg;
		setTimeout(() => {
			notification = null;
		}, 2800);
	}

	// ── Lazy load ─────────────────────────────────────────────────────────────
	function lazyLoad(node: HTMLImageElement, src: string) {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
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
			destroy() {
				observer.disconnect();
			}
		};
	}

	// ── Thumbnail URL (via Cloudinary transformations embedded in secure_url) ─
	// The Flask server returns the full secure_url; we swap dimensions for thumbs.
	function thumbUrl(picture: Picture): string {
		// If the URL is a Cloudinary URL, inject a resize transformation
		if (picture.url.includes('res.cloudinary.com')) {
			return picture.url.replace('/upload/', '/upload/w_400,h_300,c_fill,q_auto,f_auto/');
		}
		return picture.url;
	}

	function placeholderUrl(picture: Picture): string {
		if (picture.url.includes('res.cloudinary.com')) {
			return picture.url.replace('/upload/', '/upload/w_20,h_15,c_fill,q_10,e_blur:800/');
		}
		return picture.url;
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

	<!-- Error state -->
	{#if errorMsg}
		<div class="error-banner">
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
				><circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line
					x1="12"
					y1="16"
					x2="12.01"
					y2="16"
				/></svg
			>
			{errorMsg}
		</div>
	{/if}

	<!-- Skeleton or gallery -->
	{#if loading}
		<div class="grid">
			{#each Array(24), index (index)}
				<div class="card skeleton">
					<div class="skeleton-img"></div>
					<div class="skeleton-footer">
						<div class="skeleton-line short"></div>
						<div class="skeleton-line"></div>
					</div>
				</div>
			{/each}
		</div>
	{:else if pictures.length === 0 && !errorMsg}
		<div class="empty-state">
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
				><rect x="3" y="3" width="18" height="18" rx="2" /><circle
					cx="8.5"
					cy="8.5"
					r="1.5"
				/><polyline points="21 15 16 10 5 21" /></svg
			>
			<p>No images found in your Cloudinary library.</p>
			<small>Upload photos to Cloudinary and they'll appear here automatically.</small>
		</div>
	{:else}
		<div class="grid">
			{#each pictures as picture, i (picture.id)}
				<div
					class="card"
					on:click={() => openImage(picture, i)}
					on:keydown={(e) => e.key === 'Enter' && openImage(picture, i)}
					role="button"
					tabindex="0"
				>
					<div class="card-img-wrap">
						<img
							class="thumb-placeholder"
							src={placeholderUrl(picture)}
							alt=""
							aria-hidden="true"
						/>
						<img class="thumb" src="" use:lazyLoad={thumbUrl(picture)} alt="Photo by {AUTHOR}" />
						<div class="card-overlay">
							<button
								class="btn-download"
								on:click={(e) => downloadImage(picture, e)}
								aria-label="Download photo"
								disabled={downloadingId === picture.id}
							>
								{#if downloadingId === picture.id}
									<span class="spinner"></span>
								{:else}
									<svg
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2.2"
										stroke-linecap="round"
										stroke-linejoin="round"
										><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline
											points="7 10 12 15 17 10"
										/><line x1="12" y1="15" x2="12" y2="3" /></svg
									>
								{/if}
							</button>
							<div class="expand-icon">
								<svg
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
									><polyline points="15 3 21 3 21 9" /><polyline points="9 21 3 21 3 15" /><line
										x1="21"
										y1="3"
										x2="14"
										y2="10"
									/><line x1="3" y1="21" x2="10" y2="14" /></svg
								>
							</div>
						</div>
					</div>
				</div>
			{/each}
		</div>

		<!-- Load More -->
		{#if nextCursor}
			<div class="load-more-wrap">
				<button class="btn-load-more" on:click={loadMore} disabled={loadingMore}>
					{#if loadingMore}
						<span class="spinner"></span> Loading…
					{:else}
						Load more photos
					{/if}
				</button>
			</div>
		{/if}
	{/if}

	<!-- Modal lightbox -->
	{#if $selectedImage}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div
			class="modal-backdrop"
			on:click={handleModalClick}
			role="dialog"
			aria-modal="true"
			tabindex="-1"
		>
			<div class="modal-content">
				<img src={$selectedImage.url} alt="Photo by {AUTHOR}" />

				<div class="modal-info">
					<span class="modal-author">
						<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
							><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle
								cx="12"
								cy="7"
								r="4"
							/></svg
						>
						{AUTHOR}
					</span>
					<button class="btn-modal-download" on:click={(e) => downloadImage($selectedImage, e)}>
						{#if downloadingId === $selectedImage.id}
							<span class="spinner"></span> Downloading…
						{:else}
							<svg
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2.2"
								stroke-linecap="round"
								stroke-linejoin="round"
								><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline
									points="7 10 12 15 17 10"
								/><line x1="12" y1="15" x2="12" y2="3" /></svg
							>
							Download
						{/if}
					</button>
				</div>

				{#if $selectedIndex > 0}
					<button
						class="nav-btn prev"
						on:click|stopPropagation={() => navigate(-1)}
						aria-label="Previous"
					>
						<svg
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2.5"
							stroke-linecap="round"
							stroke-linejoin="round"><polyline points="15 18 9 12 15 6" /></svg
						>
					</button>
				{/if}
				{#if $selectedIndex < pictures.length - 1}
					<button
						class="nav-btn next"
						on:click|stopPropagation={() => navigate(1)}
						aria-label="Next"
					>
						<svg
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2.5"
							stroke-linecap="round"
							stroke-linejoin="round"><polyline points="9 18 15 12 9 6" /></svg
						>
					</button>
				{/if}

				<button class="modal-close" on:click={closeModal} aria-label="Close">
					<svg
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2.5"
						stroke-linecap="round"
						stroke-linejoin="round"
						><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg
					>
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
	:global(*, *::before, *::after) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}
	:global(body) {
		background-color: #0a0a0a;
		color: #e8e8e8;
		font-family:
			'Inter',
			system-ui,
			-apple-system,
			sans-serif;
	}

	/* ── HEADER ─────────────────────────────── */
	header {
		background: rgb(240, 240, 28);
		border-bottom: 1px solid rgba(255, 255, 255, 0.06);
		padding: 2rem 2.5rem 1.6rem;
		position: sticky;
		top: 0;
		z-index: 100;
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
	}
	.header-inner {
		max-width: 1600px;
		margin: 0 auto;
	}
	.brand-tagline {
		font-size: 0.8rem;
		color: #0a0a0a;
		letter-spacing: 0.04em;
		text-transform: uppercase;
	}

	/* ── ERROR / EMPTY ───────────────────────── */
	.error-banner {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		background: rgba(239, 68, 68, 0.12);
		border: 1px solid rgba(239, 68, 68, 0.35);
		color: #fca5a5;
		padding: 0.85rem 1.4rem;
		margin: 1.5rem auto;
		max-width: 700px;
		border-radius: 10px;
		font-size: 0.88rem;
	}
	.error-banner svg {
		width: 18px;
		height: 18px;
		flex-shrink: 0;
	}

	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
		padding: 6rem 2rem;
		color: #666;
		text-align: center;
	}
	.empty-state svg {
		width: 56px;
		height: 56px;
		color: #444;
	}
	.empty-state p {
		font-size: 1rem;
		color: #888;
	}
	.empty-state small {
		font-size: 0.8rem;
		color: #555;
	}

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
	.card:focus-visible {
		box-shadow: inset 0 0 0 2px #a78bfa;
	}

	.card-img-wrap {
		position: relative;
		overflow: hidden;
		aspect-ratio: 4/3;
		background: #1c1c20;
	}

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
		transition:
			opacity 0.5s ease,
			transform 0.5s ease;
	}

	.card-overlay {
		position: absolute;
		inset: 0;
		background: linear-gradient(180deg, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0.72) 100%);
		opacity: 0;
		transition: opacity 0.25s ease;
		display: flex;
		align-items: flex-end;
		justify-content: flex-end;
		padding: 0.75rem;
	}
	.card:hover .card-overlay {
		opacity: 1;
	}

	.expand-icon {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%) scale(0.85);
		transition: transform 0.2s ease;
		color: rgba(255, 255, 255, 0.8);
		pointer-events: none;
	}
	.expand-icon svg {
		width: 28px;
		height: 28px;
	}
	.card:hover .expand-icon {
		transform: translate(-50%, -50%) scale(1);
	}

	.btn-download {
		background: rgba(255, 255, 255, 0.12);
		backdrop-filter: blur(8px);
		-webkit-backdrop-filter: blur(8px);
		border: 1px solid rgba(255, 255, 255, 0.18);
		color: #fff;
		border-radius: 8px;
		padding: 0.45rem 0.55rem;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition:
			background 0.2s,
			border-color 0.2s,
			transform 0.15s;
		position: relative;
		z-index: 2;
	}
	.btn-download svg {
		width: 16px;
		height: 16px;
	}
	.btn-download:hover {
		background: rgba(167, 139, 250, 0.35);
		border-color: #a78bfa;
		transform: scale(1.07);
	}
	.btn-download:disabled {
		opacity: 0.6;
		cursor: wait;
	}

	/* ── SKELETON ────────────────────────────── */
	.skeleton .card-img-wrap {
		background: #1c1c20;
	}
	.skeleton-img {
		width: 100%;
		height: 200px;
		background: linear-gradient(90deg, #1c1c20 25%, #252529 50%, #1c1c20 75%);
		background-size: 200% 100%;
		animation: shimmer 1.5s infinite;
	}
	.skeleton-footer {
		padding: 0.65rem 0.85rem;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}
	.skeleton-line {
		height: 10px;
		border-radius: 4px;
		background: linear-gradient(90deg, #1c1c20 25%, #252529 50%, #1c1c20 75%);
		background-size: 200% 100%;
		animation: shimmer 1.5s infinite;
	}
	.skeleton-line.short {
		width: 55%;
	}
	@keyframes shimmer {
		0% {
			background-position: 200% 0;
		}
		100% {
			background-position: -200% 0;
		}
	}

	/* ── LOAD MORE ───────────────────────────── */
	.load-more-wrap {
		display: flex;
		justify-content: center;
		padding: 2.5rem 1rem;
	}
	.btn-load-more {
		display: flex;
		align-items: center;
		gap: 0.55rem;
		background: transparent;
		border: 1px solid rgba(167, 139, 250, 0.45);
		color: #a78bfa;
		padding: 0.7rem 2rem;
		border-radius: 999px;
		font-size: 0.88rem;
		font-weight: 500;
		cursor: pointer;
		transition:
			background 0.2s,
			transform 0.15s;
		letter-spacing: 0.02em;
	}
	.btn-load-more:hover {
		background: rgba(167, 139, 250, 0.12);
		transform: translateY(-1px);
	}
	.btn-load-more:disabled {
		opacity: 0.5;
		cursor: wait;
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
	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	.modal-content {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: center;
		max-width: min(92vw, 1100px);
		max-height: 92vh;
		animation: scaleIn 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
	}
	@keyframes scaleIn {
		from {
			transform: scale(0.93);
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}

	.modal-content img {
		max-width: 100%;
		max-height: calc(92vh - 60px);
		object-fit: contain;
		border-radius: 4px;
		display: block;
		box-shadow: 0 32px 80px rgba(0, 0, 0, 0.8);
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
	.modal-author svg {
		width: 14px;
		height: 14px;
	}

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
		transition:
			background 0.2s,
			transform 0.15s;
		letter-spacing: 0.01em;
	}
	.btn-modal-download svg {
		width: 15px;
		height: 15px;
	}
	.btn-modal-download:hover {
		background: #9166f0;
		transform: translateY(-1px);
	}
	.btn-modal-download:disabled {
		opacity: 0.6;
		cursor: wait;
	}

	.nav-btn {
		position: absolute;
		top: calc(50% - 30px);
		background: rgba(255, 255, 255, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.12);
		color: #fff;
		border-radius: 50%;
		width: 46px;
		height: 46px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition:
			background 0.2s,
			transform 0.15s;
		backdrop-filter: blur(6px);
		-webkit-backdrop-filter: blur(6px);
	}
	.nav-btn svg {
		width: 20px;
		height: 20px;
	}
	.nav-btn:hover {
		background: rgba(167, 139, 250, 0.3);
		border-color: #a78bfa;
		transform: scale(1.08);
	}
	.prev {
		left: -64px;
	}
	.next {
		right: -64px;
	}

	.modal-close {
		position: absolute;
		top: -48px;
		right: 0;
		background: rgba(255, 255, 255, 0.08);
		border: 1px solid rgba(255, 255, 255, 0.12);
		color: #fff;
		border-radius: 50%;
		width: 38px;
		height: 38px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition:
			background 0.2s,
			transform 0.15s;
	}
	.modal-close svg {
		width: 16px;
		height: 16px;
	}
	.modal-close:hover {
		background: rgba(239, 68, 68, 0.3);
		border-color: #ef4444;
		transform: rotate(90deg);
	}

	/* ── TOAST ───────────────────────────────── */
	.toast {
		position: fixed;
		bottom: 2rem;
		left: 50%;
		transform: translateX(-50%);
		background: #1f1f24;
		border: 1px solid rgba(167, 139, 250, 0.35);
		color: #e8e8e8;
		padding: 0.7rem 1.4rem;
		border-radius: 999px;
		font-size: 0.82rem;
		font-weight: 500;
		z-index: 2000;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
		animation:
			toastIn 0.25s ease,
			toastOut 0.3s ease 2.5s forwards;
		white-space: nowrap;
	}
	@keyframes toastIn {
		from {
			opacity: 0;
			transform: translateX(-50%) translateY(12px);
		}
		to {
			opacity: 1;
			transform: translateX(-50%) translateY(0);
		}
	}
	@keyframes toastOut {
		from {
			opacity: 1;
		}
		to {
			opacity: 0;
		}
	}

	.spinner {
		width: 14px;
		height: 14px;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-top-color: #fff;
		border-radius: 50%;
		animation: spin 0.6s linear infinite;
		display: inline-block;
	}
	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	@media (max-width: 900px) {
		.prev {
			left: -48px;
		}
		.next {
			right: -48px;
		}
	}
	@media (max-width: 640px) {
		.grid {
			grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
		}
		.prev,
		.next {
			display: none;
		}
		header {
			padding: 1.2rem 1rem 1rem;
		}
		.modal-content {
			max-width: 100vw;
			max-height: 100vh;
			border-radius: 0;
		}
		.modal-content img {
			max-height: calc(100vh - 80px);
		}
		.modal-close {
			top: 0.5rem;
			right: 0.5rem;
			position: fixed;
		}
	}
</style>
